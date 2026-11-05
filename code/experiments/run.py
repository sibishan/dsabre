import os
import io
import sys
import glob
import json
import time
import random
import contextlib
import traceback
from datetime import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.setrecursionlimit(50000)
for _p in (os.path.dirname(_HERE), _HERE):   # parent for the router, here for arch
    if _p not in sys.path:
        sys.path.insert(0, _p)

from qiskit import QuantumCircuit, qasm3
from qiskit.converters import circuit_to_dag
from qiskit.transpiler import PassManager, CouplingMap
from qiskit.transpiler.passes import RemoveBarriers, SabreLayout

from layout import adaptive_corner_count, locality_aware_layout
from dsabre_ext import dSABRE_BFSExt
from config import HardwareConfig
from verify import verify_routing
from arch import Architecture

OUT_DIR = os.path.join(_HERE, "data/out")
IN_DIR = os.path.join(_HERE, "data/in")
NUM_SEEDS = 3
RUN_DELAY_S = 3
BATCHES = [
    ("qasm_25", os.path.join(IN_DIR, "qasm_25"), Architecture.A, Architecture.A_alt),
    ("qasm_64", os.path.join(IN_DIR, "qasm_64"), Architecture.B, Architecture.B_alt),
    ("qasm_80", os.path.join(IN_DIR, "qasm_80"), Architecture.C, Architecture.C_alt),
    ("qasm_95", os.path.join(IN_DIR, "qasm_95"), Architecture.D, Architecture.D_alt),
    ("qasm_200", os.path.join(IN_DIR, "qasm_200"), Architecture.E, Architecture.E_alt),
    ("qasm_360", os.path.join(IN_DIR, "qasm_360"), Architecture.F, Architecture.F_alt),
]
# (output-file suffix, index of the arch factory in each BATCHES entry)
VARIANTS = [("", 2), ("_alt", 3)]


def bar(done, total, width=24):
    filled = int(width * done / total) if total else width
    return "[" + "#" * filled + "-" * (width - filled) + f"] {done}/{total}"


def loader(prefix, done, total, extra=""):
    """Render a single-line progress bar for the current file's runs."""
    sys.stdout.write(f"\r\033[K  {prefix} seeds {bar(done, total, 10)} {extra}")
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


def load_qasm(path):
    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("OPENQASM 3"):
                return qasm3.load(path)

            if line.startswith("OPENQASM 2"):
                return QuantumCircuit.from_qasm_file(path)

    raise ValueError(f"Unsupported OpenQASM version: {path}")


def reserved_corner_nodes(arch, per_core):
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
        return (locality_aware_layout(dag, arch, rng=random.Random(seed)),
                "locality (sabre fallback)")

    free = [p for p in arch.data_qubits if p not in set(layout.values())]
    random.Random(seed).shuffle(free)
    fp = iter(free)
    for lq in dag.qubits:
        if lq not in layout:
            layout[lq] = next(fp)
    return layout, "sabre"


def sabre_passes(router, dag, rev_dag, initial_layout):
    m1, fwd_final = router.route(dag, initial_layout)
    if m1["aborted"]:
        return None
    m2, rev_final = router.route(rev_dag, fwd_final)
    layout3 = fwd_final if m2["aborted"] else rev_final
    m3, final3 = router.route(dag, layout3)
    if m3["aborted"] or m1["eprs"] <= m3["eprs"]:
        return m1, initial_layout, fwd_final
    return m3, layout3, final3


def run_dsabre(config, qc, dag, rev_dag, arch, seed):
    router = dSABRE_BFSExt(arch, config)
    first_layout, layout_used = seed_layout(qc, dag, arch, seed)
    out = sabre_passes(router, dag, rev_dag, first_layout)
    if out is None:
        return dict(aborted=True, layout_used=layout_used)
    metrics, start_layout, final_layout = out
    return dict(
        aborted=False,
        layout_used=layout_used,
        swaps=metrics["ls"],
        teleports=metrics.get("teledata", metrics.get("teles", 0)),
        telegates=metrics.get("telegates", 0),
        circuit_depth=None,
        teleport_depth=None,
        solved_deadlocks=metrics.get("backup_activations", 0) + metrics.get("safe_routes", 0),
        start_layout=start_layout,
        final_layout=final_layout,
        trace=metrics.get("trace") or [],
    )


def run_one(config, qc, dag, rev_dag, arch, seed):
    log = io.StringIO()
    t0 = time.perf_counter()
    try:
        with contextlib.redirect_stdout(log):
            result = run_dsabre(config, qc, dag, rev_dag, arch, seed)
        exc = None
    except Exception:
        result, exc = None, traceback.format_exc(limit=3)
    runtime_s = time.perf_counter() - t0
    return result, exc, runtime_s


def run_file(qasm_path, config, arch_factory, progress=""):
    qc = load_qasm(qasm_path)
    qc = qc.remove_final_measurements(inplace=False)
    qc = PassManager([RemoveBarriers()]).run(qc)
    dag = circuit_to_dag(qc)
    rev_dag = circuit_to_dag(qc.reverse_ops())
    arch = arch_factory()

    name = os.path.basename(qasm_path)
    tag = f"{progress} {name}" if progress else name
    runs = []
    for i in range(NUM_SEEDS):
        loader(tag, i, NUM_SEEDS, extra="running...")
        result, exc, runtime_s = run_one(config, qc, dag, rev_dag, arch, i)

        if exc is not None or result['aborted']:
            runs.append({
                'seed': i,
                'layout': result['layout_used'] if result else None,
                'swaps': None, 'teleports': None, 'telegates': None,
                'circuit_depth': None, 'teleport_depth': None,
                'solved_deadlocks': None, 'solving_deadlock': exc is None,
                'num_operations': 0, 'valid': False,
                'errors': ([f"exception: {exc.strip().splitlines()[-1]}"] if exc
                           else ["run aborted (unresolved deadlock)"]),
                'runtime_s': runtime_s,
            })
        else:
            moves = [e for e in result['trace'] if e and e[0] in ("SWAP", "TELE")]
            report = verify_routing(dag, arch, result['start_layout'],
                                    result['final_layout'], moves)
            runs.append({
                'seed': i,
                'layout': result['layout_used'],
                'swaps': result['swaps'],
                'teleports': result['teleports'],
                'telegates': result['telegates'],
                'circuit_depth': result['circuit_depth'],
                'teleport_depth': result['teleport_depth'],
                'solved_deadlocks': result['solved_deadlocks'],
                'solving_deadlock': False,
                'num_operations': len(result['trace']),
                'valid': report.ok,
                'errors': list(report.failures),
                'runtime_s': runtime_s,
            })
        last = runs[-1]
        if i + 1 < NUM_SEEDS:
            loader(tag, i + 1, NUM_SEEDS,
                   extra=f"seed {i} ({last['layout']}) took {runtime_s:.1f}s")
            time.sleep(RUN_DELAY_S)
    loader(tag, NUM_SEEDS, NUM_SEEDS, extra=f"done in {sum(r['runtime_s'] for r in runs):.1f}s")

    valid_runs = [r for r in runs if not r['solving_deadlock'] and r['valid']]
    best = None
    if valid_runs:
        best = min(valid_runs, key=lambda r: (r['teleports'] + r['telegates'], r['swaps']))

    return {
        'file': name,
        'path': qasm_path,
        'arch': arch.name,
        'num_seeds': NUM_SEEDS,
        'best_seed': best['seed'] if best else None,
        'best': {
            'seed': best['seed'],
            'layout': best['layout'],
            'teleports': best['teleports'],
            'telegates': best['telegates'],
            'inter_core': best['teleports'] + best['telegates'],
            'swaps': best['swaps'],
            'circuit_depth': best['circuit_depth'],
            'valid': best['valid'],
            'errors': best['errors'],
            'runtime_s': best['runtime_s'],
        } if best else None,
        'num_valid_runs': len(valid_runs),
        'all_valid': all(r['valid'] for r in runs),
        'sabre_fallbacks': sum(1 for r in runs if "fallback" in str(r['layout'])),
        'runs': runs,
    }


def run_variant(config, suffix, arch_idx, stamp, pass_no, counter):
    print(f"===== Pass {pass_no}/{len(VARIANTS)}: dsabre_results{suffix} =====\n")
    batches = []
    for entry in BATCHES:
        label, qasm_dir = entry[0], entry[1]
        arch_factory = entry[arch_idx]
        qasm_files = sorted(glob.glob(os.path.join(qasm_dir, "*.qasm")))
        print(f"[{label}] {arch_factory.__name__}: {len(qasm_files)} qasm files in {qasm_dir}\n")

        results = []
        for path in qasm_files:
            counter['done'] += 1
            progress = (f"P{pass_no}/{len(VARIANTS)} overall "
                        f"{bar(counter['done'], counter['total'])} |")
            result = run_file(path, config, arch_factory, progress)
            results.append(result)
            if result['best']:
                b = result['best']
                print(f"    best seed={b['seed']} ({b['layout']})  inter-core={b['inter_core']}  "
                      f"swaps={b['swaps']}  depth={b['circuit_depth']}  valid={b['valid']}")
            else:
                print("    no valid run (all deadlocked, failed validation or raised)")
            if result['sabre_fallbacks']:
                print(f"    WARNING: SabreLayout fell back to locality-aware layout on "
                      f"{result['sabre_fallbacks']} seed(s)")
            for r in result['runs']:
                if r['errors'] and r['errors'][0].startswith("exception"):
                    print(f"    seed {r['seed']} FAILED: {r['errors'][0]}")
                elif not r['valid'] and not r['solving_deadlock']:
                    print(f"    seed {r['seed']} INVALID: {r['errors'][:3]}")

        batches.append({
            'batch': label,
            'qasm_dir': qasm_dir,
            'results': results,
        })
        print()

    payload = {
        'generated_at': datetime.now().isoformat(),
        'variant': suffix.lstrip('_') or 'base',
        'num_seeds': NUM_SEEDS,
        'layout_protocol': (f"SabreLayout (locality-aware fallback) on all "
                            f"{NUM_SEEDS} seeds; best by (EPR, SWAPs)"),
        'config': json_safe(vars(config)),
        'batches': batches,
    }

    out_path = os.path.join(OUT_DIR, f"dsabre_results{suffix}_{stamp}.json")
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote results to {out_path}\n")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    config = HardwareConfig(deadlock_limit=None, max_backup_attempts=None,
                            max_iterations=None, trace_routing=True)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    files_per_pass = sum(len(glob.glob(os.path.join(d, "*.qasm"))) for _, d, *_ in BATCHES)
    counter = {'done': 0, 'total': files_per_pass * len(VARIANTS)}
    for pass_no, (suffix, arch_idx) in enumerate(VARIANTS, 1):
        run_variant(config, suffix, arch_idx, stamp, pass_no, counter)


if __name__ == "__main__":
    main()
