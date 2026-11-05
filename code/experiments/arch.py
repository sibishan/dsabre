import networkx as nx

from architecture import DistributedArchitecture

# Device A: four 4x4 cores, ring 0-2-3-1-0, 64 qubits.
A_NAME = "A"
A_NUM_CORES = 4
A_CORE_ROWS = 4
A_CORE_COLS = 4
A_QUBITS_PER_CORE = A_CORE_ROWS * A_CORE_COLS
A_NUM_QUBITS = A_NUM_CORES * A_QUBITS_PER_CORE

A_INTER_CORE_EDGES = [(12, 32), (47, 60), (51, 31), (16, 3)]

# Device B: four 5x5 cores, ring 0-1-3-2-0, 100 qubits.
B_NAME = "B"
B_NUM_CORES = 4
B_CORE_ROWS = 5
B_CORE_COLS = 5
B_QUBITS_PER_CORE = B_CORE_ROWS * B_CORE_COLS
B_NUM_QUBITS = B_NUM_CORES * B_QUBITS_PER_CORE

B_INTER_CORE_EDGES = [(4, 25), (49, 79), (95, 74), (50, 20)]

# Device C: four 6x5 cores, ring 0-1-3-2-0, 120 qubits.
C_NAME = "C"
C_NUM_CORES = 4
C_CORE_ROWS = 6
C_CORE_COLS = 5
C_QUBITS_PER_CORE = C_CORE_ROWS * C_CORE_COLS
C_NUM_QUBITS = C_NUM_CORES * C_QUBITS_PER_CORE

C_INTER_CORE_EDGES = [(4, 30), (25, 60), (89, 115), (59, 94)]

# Device D: six 5x5 cores in a 2x3 core grid, 150 qubits.
D_NAME = "D"
D_NUM_CORES = 6
D_CORE_ROWS = 5
D_CORE_COLS = 5
D_QUBITS_PER_CORE = D_CORE_ROWS * D_CORE_COLS
D_NUM_QUBITS = D_NUM_CORES * D_QUBITS_PER_CORE

D_INTER_CORE_EDGES = [
    (4, 25), (20, 75), (29, 50), (47, 102), (74, 129), (99, 120), (124, 145),
]

# Device E: eight 7x5 cores in a 2x4 core grid, 280 qubits.
E_NAME = "E"
E_NUM_CORES = 8
E_CORE_ROWS = 7
E_CORE_COLS = 5
E_QUBITS_PER_CORE = E_CORE_ROWS * E_CORE_COLS
E_NUM_QUBITS = E_NUM_CORES * E_QUBITS_PER_CORE

E_INTER_CORE_EDGES = [
    (4, 35), (39, 70), (74, 105), (139, 249), (244, 275), (209, 240),
    (174, 205), (30, 140), (67, 177), (102, 212),
]

# Device F: twelve 7x6 cores in a 3x4 core grid, 504 qubits.
F_NAME = "F"
F_NUM_CORES = 12
F_CORE_ROWS = 7
F_CORE_COLS = 6
F_QUBITS_PER_CORE = F_CORE_ROWS * F_CORE_COLS
F_NUM_QUBITS = F_NUM_CORES * F_QUBITS_PER_CORE

F_INTER_CORE_EDGES = [
    (5, 42), (47, 84), (89, 126), (191, 228), (233, 270), (275, 312),
    (377, 414), (419, 456), (461, 498), (36, 168), (80, 212), (122, 254),
    (167, 299), (204, 336), (248, 380), (290, 422), (335, 467),
]

# Device A_alt: four 4x3 cores, ring 0-1-3-2-0, 48 qubits.
A_ALT_NAME = "A_alt"
A_ALT_NUM_CORES = 4
A_ALT_CORE_ROWS = 4
A_ALT_CORE_COLS = 3
A_ALT_QUBITS_PER_CORE = A_ALT_CORE_ROWS * A_ALT_CORE_COLS
A_ALT_NUM_QUBITS = A_ALT_NUM_CORES * A_ALT_QUBITS_PER_CORE

A_ALT_INTER_CORE_EDGES = [(2, 12), (9, 24), (23, 38), (35, 45)]

# Device B_alt: four 5x4 cores, ring 0-1-3-2-0, 80 qubits.
B_ALT_NAME = "B_alt"
B_ALT_NUM_CORES = 4
B_ALT_CORE_ROWS = 5
B_ALT_CORE_COLS = 4
B_ALT_QUBITS_PER_CORE = B_ALT_CORE_ROWS * B_ALT_CORE_COLS
B_ALT_NUM_QUBITS = B_ALT_NUM_CORES * B_ALT_QUBITS_PER_CORE

B_ALT_INTER_CORE_EDGES = [(3, 20), (16, 40), (39, 63), (59, 76)]

# Device C_alt: four 6x4 cores, ring 0-1-3-2-0, 96 qubits.
C_ALT_NAME = "C_alt"
C_ALT_NUM_CORES = 4
C_ALT_CORE_ROWS = 6
C_ALT_CORE_COLS = 4
C_ALT_QUBITS_PER_CORE = C_ALT_CORE_ROWS * C_ALT_CORE_COLS
C_ALT_NUM_QUBITS = C_ALT_NUM_CORES * C_ALT_QUBITS_PER_CORE

C_ALT_INTER_CORE_EDGES = [(3, 24), (20, 48), (47, 75), (71, 92)]

# Device D_alt: six 5x4 cores in a 2x3 core grid, 120 qubits.
D_ALT_NAME = "D_alt"
D_ALT_NUM_CORES = 6
D_ALT_CORE_ROWS = 5
D_ALT_CORE_COLS = 4
D_ALT_QUBITS_PER_CORE = D_ALT_CORE_ROWS * D_ALT_CORE_COLS
D_ALT_NUM_QUBITS = D_ALT_NUM_CORES * D_ALT_QUBITS_PER_CORE

D_ALT_INTER_CORE_EDGES = [
    (3, 20), (16, 60), (23, 40), (38, 82), (59, 103), (79, 96), (99, 116),
]

# Device E_alt: eight 6x5 cores in a 2x4 core grid, 240 qubits.
E_ALT_NAME = "E_alt"
E_ALT_NUM_CORES = 8
E_ALT_CORE_ROWS = 6
E_ALT_CORE_COLS = 5
E_ALT_QUBITS_PER_CORE = E_ALT_CORE_ROWS * E_ALT_CORE_COLS
E_ALT_NUM_QUBITS = E_ALT_NUM_CORES * E_ALT_QUBITS_PER_CORE

E_ALT_INTER_CORE_EDGES = [
    (4, 30), (34, 60), (64, 90), (119, 214), (209, 235), (179, 205),
    (149, 175), (25, 120), (57, 152), (87, 182),
]

# Device F_alt: twelve 6x6 cores in a 3x4 core grid, 432 qubits.
F_ALT_NAME = "F_alt"
F_ALT_NUM_CORES = 12
F_ALT_CORE_ROWS = 6
F_ALT_CORE_COLS = 6
F_ALT_QUBITS_PER_CORE = F_ALT_CORE_ROWS * F_ALT_CORE_COLS
F_ALT_NUM_QUBITS = F_ALT_NUM_CORES * F_ALT_QUBITS_PER_CORE

F_ALT_INTER_CORE_EDGES = [
    (5, 36), (41, 72), (77, 108), (143, 257), (287, 401), (395, 426),
    (359, 390), (323, 354), (174, 288), (30, 144), (69, 183), (105, 219),
    (167, 198), (203, 234), (239, 270), (213, 327), (249, 363),
]


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


def _build(name: str, num_cores: int, rows: int, cols: int,
           inter_edges) -> DistributedArchitecture:
    intra_graphs = {c: _core_grid(c, rows, cols) for c in range(num_cores)}
    arch = DistributedArchitecture(intra_graphs, list(inter_edges))
    arch.name = name
    return arch


def build_a_architecture() -> DistributedArchitecture:
    """The 64-qubit, 4-core device A."""
    return _build(A_NAME, A_NUM_CORES, A_CORE_ROWS, A_CORE_COLS,
                  A_INTER_CORE_EDGES)


def build_b_architecture() -> DistributedArchitecture:
    """The 100-qubit, 4-core device B."""
    return _build(B_NAME, B_NUM_CORES, B_CORE_ROWS, B_CORE_COLS,
                  B_INTER_CORE_EDGES)


def build_c_architecture() -> DistributedArchitecture:
    """The 120-qubit, 4-core device C."""
    return _build(C_NAME, C_NUM_CORES, C_CORE_ROWS, C_CORE_COLS,
                  C_INTER_CORE_EDGES)


def build_d_architecture() -> DistributedArchitecture:
    """The 150-qubit, 6-core device D."""
    return _build(D_NAME, D_NUM_CORES, D_CORE_ROWS, D_CORE_COLS,
                  D_INTER_CORE_EDGES)


def build_e_architecture() -> DistributedArchitecture:
    """The 280-qubit, 8-core device E."""
    return _build(E_NAME, E_NUM_CORES, E_CORE_ROWS, E_CORE_COLS,
                  E_INTER_CORE_EDGES)


def build_f_architecture() -> DistributedArchitecture:
    """The 504-qubit, 12-core device F."""
    return _build(F_NAME, F_NUM_CORES, F_CORE_ROWS, F_CORE_COLS,
                  F_INTER_CORE_EDGES)


def build_a_alt_architecture() -> DistributedArchitecture:
    """The 48-qubit, 4-core device A_alt."""
    return _build(A_ALT_NAME, A_ALT_NUM_CORES, A_ALT_CORE_ROWS, A_ALT_CORE_COLS,
                  A_ALT_INTER_CORE_EDGES)


def build_b_alt_architecture() -> DistributedArchitecture:
    """The 80-qubit, 4-core device B_alt."""
    return _build(B_ALT_NAME, B_ALT_NUM_CORES, B_ALT_CORE_ROWS, B_ALT_CORE_COLS,
                  B_ALT_INTER_CORE_EDGES)


def build_c_alt_architecture() -> DistributedArchitecture:
    """The 96-qubit, 4-core device C_alt."""
    return _build(C_ALT_NAME, C_ALT_NUM_CORES, C_ALT_CORE_ROWS, C_ALT_CORE_COLS,
                  C_ALT_INTER_CORE_EDGES)


def build_d_alt_architecture() -> DistributedArchitecture:
    """The 120-qubit, 6-core device D_alt."""
    return _build(D_ALT_NAME, D_ALT_NUM_CORES, D_ALT_CORE_ROWS, D_ALT_CORE_COLS,
                  D_ALT_INTER_CORE_EDGES)


def build_e_alt_architecture() -> DistributedArchitecture:
    """The 240-qubit, 8-core device E_alt."""
    return _build(E_ALT_NAME, E_ALT_NUM_CORES, E_ALT_CORE_ROWS, E_ALT_CORE_COLS,
                  E_ALT_INTER_CORE_EDGES)


def build_f_alt_architecture() -> DistributedArchitecture:
    """The 432-qubit, 12-core device F_alt."""
    return _build(F_ALT_NAME, F_ALT_NUM_CORES, F_ALT_CORE_ROWS, F_ALT_CORE_COLS,
                  F_ALT_INTER_CORE_EDGES)


class Architecture:
    """Device factories by name: `Architecture.A()` builds device A."""
    A = staticmethod(build_a_architecture)
    B = staticmethod(build_b_architecture)
    C = staticmethod(build_c_architecture)
    D = staticmethod(build_d_architecture)
    E = staticmethod(build_e_architecture)
    F = staticmethod(build_f_architecture)
    A_alt = staticmethod(build_a_alt_architecture)
    B_alt = staticmethod(build_b_alt_architecture)
    C_alt = staticmethod(build_c_alt_architecture)
    D_alt = staticmethod(build_d_alt_architecture)
    E_alt = staticmethod(build_e_alt_architecture)
    F_alt = staticmethod(build_f_alt_architecture)
