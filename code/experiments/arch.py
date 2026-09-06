import networkx as nx

from architecture import DistributedArchitecture

# Device G: four 4x4 cores (64 qubits), cores wired into the ring 0-2-3-1-0.
G_NAME = "G"
G_NUM_CORES = 4
G_CORE_ROWS = 4         # each core is G_CORE_ROWS x G_CORE_COLS
G_CORE_COLS = 4
G_QUBITS_PER_CORE = G_CORE_ROWS * G_CORE_COLS
G_NUM_QUBITS = G_NUM_CORES * G_QUBITS_PER_CORE

# Endpoints as given by the device spec, in spec order.
G_INTER_CORE_EDGES = [(12, 32), (47, 60), (51, 31), (16, 3)]

# Device H: four 5x5 cores (100 qubits), cores wired into the ring 0-1-3-2-0.
H_NAME = "H"
H_NUM_CORES = 4
H_CORE_ROWS = 5
H_CORE_COLS = 5
H_QUBITS_PER_CORE = H_CORE_ROWS * H_CORE_COLS
H_NUM_QUBITS = H_NUM_CORES * H_QUBITS_PER_CORE

H_INTER_CORE_EDGES = [(4, 25), (49, 79), (95, 74), (50, 20)]

# Device I: four 6x6 cores (144 qubits), cores wired into the ring 0-1-3-2-0.
I_NAME = "I"
I_NUM_CORES = 4
I_CORE_ROWS = 6
I_CORE_COLS = 6
I_QUBITS_PER_CORE = I_CORE_ROWS * I_CORE_COLS
I_NUM_QUBITS = I_NUM_CORES * I_QUBITS_PER_CORE

I_INTER_CORE_EDGES = [(5, 36), (30, 72), (107, 138), (113, 71)]

# Device J: four 7x7 cores (196 qubits), cores wired into the ring 0-1-3-2-0.
J_NAME = "J"
J_NUM_CORES = 4
J_CORE_ROWS = 7
J_CORE_COLS = 7
J_QUBITS_PER_CORE = J_CORE_ROWS * J_CORE_COLS
J_NUM_QUBITS = J_NUM_CORES * J_QUBITS_PER_CORE

J_INTER_CORE_EDGES = [(6, 49), (42, 98), (146, 189), (153, 97)]

# Device K: four 8x8 cores (256 qubits), cores wired into the ring 0-1-3-2-0.
K_NAME = "K"
K_NUM_CORES = 4
K_CORE_ROWS = 8
K_CORE_COLS = 8
K_QUBITS_PER_CORE = K_CORE_ROWS * K_CORE_COLS
K_NUM_QUBITS = K_NUM_CORES * K_QUBITS_PER_CORE

K_INTER_CORE_EDGES = [(7, 64), (56, 128), (191, 248), (199, 127)]

# Device L: four 10x10 cores (400 qubits), cores wired into the ring 0-1-3-2-0.
L_NAME = "L"
L_NUM_CORES = 4
L_CORE_ROWS = 10
L_CORE_COLS = 10
L_QUBITS_PER_CORE = L_CORE_ROWS * L_CORE_COLS
L_NUM_QUBITS = L_NUM_CORES * L_QUBITS_PER_CORE

L_INTER_CORE_EDGES = [(9, 100), (90, 200), (299, 390), (309, 199)]


def _gid(core: int, row: int, col: int, rows: int, cols: int) -> int:
    """Global id of the qubit at (row, col) of `core` in a rows x cols core."""
    return core * rows * cols + row * cols + col


def _core_grid(core: int, rows: int, cols: int) -> nx.Graph:
    """One core: a rows x cols nearest-neighbour grid, unit weights."""
    g = nx.Graph()
    for r in range(rows):
        for c in range(cols):
            u = _gid(core, r, c, rows, cols)
            g.add_node(u)
            if c + 1 < cols:
                g.add_edge(u, _gid(core, r, c + 1, rows, cols), weight=1)
            if r + 1 < rows:
                g.add_edge(u, _gid(core, r + 1, c, rows, cols), weight=1)
    return g


def build_g_architecture() -> DistributedArchitecture:
    """The 64-qubit, 4-core device G."""
    intra_graphs = {c: _core_grid(c, G_CORE_ROWS, G_CORE_COLS)
                    for c in range(G_NUM_CORES)}
    return DistributedArchitecture(intra_graphs, list(G_INTER_CORE_EDGES))


def build_h_architecture() -> DistributedArchitecture:
    """The 100-qubit, 4-core device J."""
    intra_graphs = {c: _core_grid(c, H_CORE_ROWS, H_CORE_COLS)
                    for c in range(H_NUM_CORES)}
    return DistributedArchitecture(intra_graphs, list(H_INTER_CORE_EDGES))


def build_i_architecture() -> DistributedArchitecture:
    """The 144-qubit, 4-core device I."""
    intra_graphs = {c: _core_grid(c, I_CORE_ROWS, I_CORE_COLS)
                    for c in range(I_NUM_CORES)}
    return DistributedArchitecture(intra_graphs, list(I_INTER_CORE_EDGES))


def build_j_architecture() -> DistributedArchitecture:
    """The 196-qubit, 4-core device J."""
    intra_graphs = {c: _core_grid(c, J_CORE_ROWS, J_CORE_COLS)
                    for c in range(J_NUM_CORES)}
    return DistributedArchitecture(intra_graphs, list(J_INTER_CORE_EDGES))


def build_k_architecture() -> DistributedArchitecture:
    """The 256-qubit, 4-core device K."""
    intra_graphs = {c: _core_grid(c, K_CORE_ROWS, K_CORE_COLS)
                    for c in range(K_NUM_CORES)}
    return DistributedArchitecture(intra_graphs, list(K_INTER_CORE_EDGES))


def build_l_architecture() -> DistributedArchitecture:
    """The 400-qubit, 4-core device L."""
    intra_graphs = {c: _core_grid(c, L_CORE_ROWS, L_CORE_COLS)
                    for c in range(L_NUM_CORES)}
    return DistributedArchitecture(intra_graphs, list(L_INTER_CORE_EDGES))
