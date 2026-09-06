import os
import sys
import glob
import json
import time
import random
from datetime import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.setrecursionlimit(50000)
for _p in (os.path.dirname(_HERE), _HERE):   # parent for the router, here for arch
    if _p not in sys.path:
        sys.path.insert(0, _p)

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.transpiler import PassManager, CouplingMap
from qiskit.transpiler.passes import RemoveBarriers, SabreLayout

from layout import (adaptive_corner_count, locality_aware_layout,
                    run_sabre_passes)
from dsabre_ext import dSABRE_BFSExt
from config import HardwareConfig
from arch import build_g_architecture, build_h_architecture, build_i_architecture, build_j_architecture, build_k_architecture, build_l_architecture

OUT_DIR = os.path.join(_HERE, "data/out")
NUM_SEEDS = 10
BATCHES = [
    ("qasm_25", os.path.join(_HERE, "data/in/qasm_25"), build_g_architecture),
    ("qasm_64", os.path.join(_HERE, "data/in/qasm_64"), build_h_architecture),
    ("qasmm_100", os.path.join(_HERE, "data/in/qasm_100"), build_i_architecture),
    ("qasm_160", os.path.join(_HERE, "data/in/qasm_160"), build_j_architecture),
    ("qasm_200", os.path.join(_HERE, "data/in/qasm_200"), build_k_architecture),
    ("qasm_360", os.path.join(_HERE, "data/in/qasm_360"), build_l_architecture),
]


def loader(prefix, done, total, extra=""):
    """Render a single-line progress bar for the current file's runs."""
    width = 24
    filled = int(width * done / total) if total else width
    bar = "#" * filled + "-" * (width - filled)
    sys.stdout.write(f"\r  {prefix} [{bar}] {done}/{total} {extra}")
    sys.stdout.flush()
    if done >= total:
        sys.stdout.write("\n")
        sys.stdout.flush()


def json_safe(obj):
    """Recursively convert an object into something json.dump can handle."""
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    return str(obj)


def reserved_corner_nodes(arch, per_core):
    """`layout._per_core_reserved_corner_nodes`, minus the comm ports.

    The library version reserves each core's most-remote minimum-degree
    vertices as escape slots.  On G and J the inter-core links land ON grid
    corners, so a core has fewer than `per_core` degree-2 vertices, the
    library's fallback widens the candidate set by (degree, id), and a comm
    port -- degree 3, like every grid edge node, and low-numbered -- gets
    reserved.  Removing a port disconnects the coupling map handed to
    SabreLayout, which then raises for the 64q circuits and, worse, silently
    succeeds for the 25q ones on a device picture with no links in it.
    Excluding ports up front is a no-op on the paper's architectures, whose
    ports sit on boundary mid-rows and never trip the fallback.
    """
    if per_core <= 0:
        return set()
    ports = set(arch.comm_qubits)
    reserved = set()
    for c in range(arch.num_cores):
        nodes = [n for n in arch.core_qubits(c) if n not in ports]
        degs = {n: arch.Gr.degree(n) for n in nodes}
        min_deg = min(degs.values())
        cands = [n for n in nodes if degs[n] == min_deg]
        if len(cands) < per_core:
            cands = sorted(nodes, key=lambda n: (degs[n], n))[:per_core]
        remote = {n: sum(arch.phys_dist[n].get(q, 0) for q in arch.data_qubits)
                  for n in cands}
        reserved.update(sorted(cands, key=lambda n: (-remote[n], n))[:per_core])
    return reserved


def seed_layout(qc, dag, arch, seed):
    """One initial layout for `seed`: SabreLayout with reserved corners removed.

    Falls back to `locality_aware_layout` if SabreLayout cannot place the
    circuit, so a seed always yields a layout to route.
    """
    corners = reserved_corner_nodes(arch, adaptive_corner_count(arch, qc.num_qubits))
    reduced = [n for n in arch.Gr.nodes() if n not in corners]
    idx = {n: i for i, n in enumerate(reduced)}
    edges = [(idx[u], idx[v]) for u, v in arch.Gr.edges()
             if u not in corners and v not in corners]

    layout = {}
    try:
        cm = CouplingMap(couplinglist=edges + [(v, u) for u, v in edges])
        pm = PassManager([SabreLayout(cm, max_iterations=3, seed=seed,
                                      swap_trials=5)])
        transpiled = pm.run(qc)
        tl = transpiled.layout
        virt = (tl.initial_virtual_layout(filter_ancillas=True)
                if hasattr(tl, "initial_virtual_layout") else tl.initial_layout)
        for virt_qubit, reduced_idx in virt.get_virtual_bits().items():
            try:
                bit_index = qc.find_bit(virt_qubit).index
            except Exception:
                continue
            layout[dag.qubits[bit_index]] = reduced[reduced_idx]
    except Exception:
        return locality_aware_layout(dag, arch, rng=random.Random(seed))

    free = [p for p in arch.data_qubits if p not in set(layout.values())]
    random.Random(seed).shuffle(free)
    fp = iter(free)
    for lq in dag.qubits:
        if lq not in layout:
            layout[lq] = next(fp)
    return layout


def run_dsabre(config, qc, dag, rev_dag, arch, seed):
    """Route `dag` once from `seed`'s layout, in run_boltsabre's return shape.

    circuit_depth / teleport_depth come back None: this router reports EPR and
    SWAP counts against a layout, and never materialises a scheduled circuit,
    so there is no depth to measure without new instrumentation in router.py.
    """
    router = dSABRE_BFSExt(arch, config)
    first_layout = seed_layout(qc, dag, arch, seed)
    metrics = run_sabre_passes(router, dag, rev_dag, first_layout)

    if metrics is None or metrics.get("aborted"):
        return (0, 0, 0, None, None, 0, first_layout, True, [], [])

    trace = metrics.get("trace") or []
    return (
        metrics["ls"],                                    # swap_count
        metrics.get("teledata", metrics.get("teles", 0)),  # teleportation_count
        metrics.get("telegates", 0),                      # telegate_count
        None,                                             # circuit_depth
        None,                                             # teleport_depth
        metrics.get("backup_activations", 0) + metrics.get("safe_routes", 0),
        first_layout,                                     # first_layout
        False,                                            # solving_deadlock
        trace,                                            # operations
        [e for e in trace if e and e[0] in ("TELE", "TGATE")],  # teleport_log
    )


def run_file(qasm_path, config, arch_factory):
    qc = QuantumCircuit.from_qasm_file(qasm_path)
    # route() rejects >2-qubit operations, and a barrier spanning every wire
    # is one, so stripping them is load-bearing rather than cosmetic.
    qc = qc.remove_final_measurements(inplace=False)
    qc = PassManager([RemoveBarriers()]).run(qc)
    dag = circuit_to_dag(qc)
    rev_dag = circuit_to_dag(qc.reverse_ops())
    arch = arch_factory()

    name = os.path.basename(qasm_path)
    runs = []
    start = time.time()
    for i in range(NUM_SEEDS):
        loader(name, i, NUM_SEEDS, extra="running...")
        (swap_count, teleportation_count, telegate_count, circuit_depth, teleport_depth,
        solved_deadlocks, first_layout, solving_deadlock, operations, teleport_log) \
            = run_dsabre(config, qc, dag, rev_dag, arch, seed=i)
        runs.append({
            'seed': i,
            'swaps': swap_count,
            'teleports': teleportation_count,
            'telegates': telegate_count,
            'circuit_depth': circuit_depth,
            'teleport_depth': teleport_depth,
            'solved_deadlocks': solved_deadlocks,
            'solving_deadlock': solving_deadlock,
            'num_operations': len(operations),
            'teleport_log': json_safe(teleport_log),
            # 'operations': json_safe(operations),
        })
    loader(name, NUM_SEEDS, NUM_SEEDS, extra=f"done in {time.time() - start:.1f}s")

    valid_runs = [r for r in runs if not r['solving_deadlock']]
    best = None
    if valid_runs:
        best = min(valid_runs, key=lambda r: r['teleports'] + r['telegates'])

    return {
        'file': name,
        'path': qasm_path,
        'num_seeds': NUM_SEEDS,
        'best_seed': best['seed'] if best else None,
        'best': {
            'seed': best['seed'],
            'teleports': best['teleports'],
            'telegates': best['telegates'],
            'inter_core': best['teleports'] + best['telegates'],
            'swaps': best['swaps'],
            'circuit_depth': best['circuit_depth'],
        } if best else None,
        'num_valid_runs': len(valid_runs),
        'runs': runs,
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    # telegate=True offers the cat-comm action alongside teledata, so the
    # telegate column is a measurement rather than a constant 0.  The three
    # recovery budgets stay None: they are derived per architecture at route()
    # entry, which is what every driver on the reproduction path passes.
    config = HardwareConfig(deadlock_limit=None, max_backup_attempts=None,
                     max_iterations=None)

    batches = []
    for label, qasm_dir, arch_factory in BATCHES:
        qasm_files = sorted(glob.glob(os.path.join(qasm_dir, "*.qasm")))
        print(f"[{label}] {len(qasm_files)} qasm files in {qasm_dir}\n")

        results = []
        for path in qasm_files:
            result = run_file(path, config, arch_factory)
            results.append(result)
            if result['best']:
                b = result['best']
                print(f"    best seed={b['seed']}  inter-core={b['inter_core']}  "
                      f"swaps={b['swaps']}  depth={b['circuit_depth']}")
            else:
                print("    all runs ended in unresolved deadlock")

        batches.append({
            'batch': label,
            'qasm_dir': qasm_dir,
            'results': results,
        })
        print()

    payload = {
        'generated_at': datetime.now().isoformat(),
        'num_seeds': NUM_SEEDS,
        'batches': batches,
    }

    out_path = os.path.join(
        OUT_DIR, f"dsabre_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nWrote results to {out_path}")


if __name__ == "__main__":
    main()
