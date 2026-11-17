import networkx as nx

from architecture import DistributedArchitecture

# Devices A-I: core grids and inter-core (communication) edges match
# BOLTSabre's A_alt..I_alt. Their buffer edges are ignored here.

# Device A: four 4x4 cores in a 2x2 core grid, 64 qubits.
A_NAME = "A"
A_NUM_CORES = 4
A_CORE_ROWS = 4
A_CORE_COLS = 4
A_QUBITS_PER_CORE = A_CORE_ROWS * A_CORE_COLS
A_NUM_QUBITS = A_NUM_CORES * A_QUBITS_PER_CORE

A_INTER_CORE_EDGES = [(3, 16), (12, 32), (47, 60), (51, 31)]

# Device B: four 5x5 cores in a 2x2 core grid, 100 qubits.
B_NAME = "B"
B_NUM_CORES = 4
B_CORE_ROWS = 5
B_CORE_COLS = 5
B_QUBITS_PER_CORE = B_CORE_ROWS * B_CORE_COLS
B_NUM_QUBITS = B_NUM_CORES * B_QUBITS_PER_CORE

B_INTER_CORE_EDGES = [(4, 25), (20, 50), (74, 95), (79, 49)]

# Device C: four 6x5 cores (6 rows, 5 cols) in a 2x2 core grid, 120 qubits.
C_NAME = "C"
C_NUM_CORES = 4
C_CORE_ROWS = 6
C_CORE_COLS = 5
C_QUBITS_PER_CORE = C_CORE_ROWS * C_CORE_COLS
C_NUM_QUBITS = C_NUM_CORES * C_QUBITS_PER_CORE

C_INTER_CORE_EDGES = [(4, 30), (25, 60), (89, 115), (59, 94)]

# Device D: six 5x5 cores in a 3x2 core grid, 150 qubits.
D_NAME = "D"
D_NUM_CORES = 6
D_CORE_ROWS = 5
D_CORE_COLS = 5
D_QUBITS_PER_CORE = D_CORE_ROWS * D_CORE_COLS
D_NUM_QUBITS = D_NUM_CORES * D_QUBITS_PER_CORE

D_INTER_CORE_EDGES = [
    (4, 25), (29, 50), (74, 129), (124, 145), (99, 120), (20, 75), (47, 102),
]

# Device E: eight 7x5 cores (7 rows, 5 cols) in a 4x2 core grid, 280 qubits.
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

# Device F: twelve 7x6 cores (7 rows, 6 cols) in a 4x3 core grid, 504 qubits.
F_NAME = "F"
F_NUM_CORES = 12
F_CORE_ROWS = 7
F_CORE_COLS = 6
F_QUBITS_PER_CORE = F_CORE_ROWS * F_CORE_COLS
F_NUM_QUBITS = F_NUM_CORES * F_QUBITS_PER_CORE

F_INTER_CORE_EDGES = [
    (5, 42), (47, 84), (89, 126), (191, 228), (233, 270), (275, 312),
    (377, 414), (419, 456), (461, 498), (36, 168), (80, 212), (122, 254),
    (167, 299), (204, 336), (249, 381), (291, 423), (335, 467),
]

# Device G: fifteen 8x6 cores (8 rows, 6 cols) in a 5x3 core grid, 720 qubits.
G_NAME = "G"
G_NUM_CORES = 15
G_CORE_ROWS = 8
G_CORE_COLS = 6
G_QUBITS_PER_CORE = G_CORE_ROWS * G_CORE_COLS
G_NUM_QUBITS = G_NUM_CORES * G_QUBITS_PER_CORE

G_INTER_CORE_EDGES = [
    (5, 48), (53, 96), (101, 144), (149, 192), (263, 306), (317, 360),
    (359, 402), (413, 456), (527, 570), (575, 618), (623, 666), (671, 714),
    (42, 240), (92, 290), (140, 338), (188, 386), (239, 437), (282, 480),
    (333, 531), (381, 579), (429, 627), (479, 677),
]

# Device H: twenty 11x6 cores (11 rows, 6 cols) in a 5x4 core grid,
# 1320 qubits.
H_NAME = "H"
H_NUM_CORES = 20
H_CORE_ROWS = 11
H_CORE_COLS = 6
H_QUBITS_PER_CORE = H_CORE_ROWS * H_CORE_COLS
H_NUM_QUBITS = H_NUM_CORES * H_QUBITS_PER_CORE

H_INTER_CORE_EDGES = [
    (5, 66), (71, 132), (137, 198), (203, 264), (365, 426), (431, 492),
    (497, 558), (563, 624), (695, 756), (761, 822), (827, 888), (893, 954),
    (1055, 1116), (1121, 1182), (1187, 1248), (1253, 1314),
    (60, 330), (128, 398), (194, 464), (260, 530), (329, 599), (390, 660),
    (459, 729), (525, 795), (591, 861), (659, 929), (720, 990), (788, 1058),
    (854, 1124), (920, 1190), (989, 1259),
]

# Device I: thirty 11x6 cores (11 rows, 6 cols) in a 6x5 core grid,
# 1980 qubits.
I_NAME = "I"
I_NUM_CORES = 30
I_CORE_ROWS = 11
I_CORE_COLS = 6
I_QUBITS_PER_CORE = I_CORE_ROWS * I_CORE_COLS
I_NUM_QUBITS = I_NUM_CORES * I_QUBITS_PER_CORE

I_INTER_CORE_EDGES = [
    (5, 66), (71, 132), (137, 198), (203, 264), (269, 330),
    (431, 492), (497, 558), (563, 624), (629, 690), (695, 756),
    (827, 888), (893, 954), (959, 1020), (1025, 1086), (1091, 1152),
    (1223, 1284), (1289, 1350), (1355, 1416), (1421, 1482), (1487, 1548),
    (1649, 1710), (1715, 1776), (1781, 1842), (1847, 1908), (1913, 1974),
    (60, 396), (128, 464), (194, 530), (260, 596), (326, 662),
    (395, 731), (456, 792), (525, 861), (591, 927), (657, 993), (723, 1059),
    (791, 1127), (852, 1188), (920, 1256), (986, 1322), (1052, 1388),
    (1118, 1454), (1187, 1523), (1248, 1584), (1317, 1653), (1383, 1719),
    (1449, 1785), (1515, 1851), (1583, 1919),
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


def build_g_architecture() -> DistributedArchitecture:
    """The 720-qubit, 15-core device G."""
    return _build(G_NAME, G_NUM_CORES, G_CORE_ROWS, G_CORE_COLS,
                  G_INTER_CORE_EDGES)


def build_h_architecture() -> DistributedArchitecture:
    """The 1320-qubit, 20-core device H."""
    return _build(H_NAME, H_NUM_CORES, H_CORE_ROWS, H_CORE_COLS,
                  H_INTER_CORE_EDGES)


def build_i_architecture() -> DistributedArchitecture:
    """The 1980-qubit, 30-core device I."""
    return _build(I_NAME, I_NUM_CORES, I_CORE_ROWS, I_CORE_COLS,
                  I_INTER_CORE_EDGES)


class Architecture:
    """Device factories by name: `Architecture.A()` builds device A."""
    A = staticmethod(build_a_architecture)
    B = staticmethod(build_b_architecture)
    C = staticmethod(build_c_architecture)
    D = staticmethod(build_d_architecture)
    E = staticmethod(build_e_architecture)
    F = staticmethod(build_f_architecture)
    G = staticmethod(build_g_architecture)
    H = staticmethod(build_h_architecture)
    I = staticmethod(build_i_architecture)
