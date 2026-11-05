# MPI MATRIX MULTIPLICATION (mpi4py)   run:  mpiexec -n 3 python mpi_matrix.py
# every process runs this same file; rank tells it who it is (0 = master)
# steps: BROADCAST B -> SCATTER rows of A -> each rank computes its rows -> GATHER rows of C
# C[i][j] = sum over k of A[i][k] * B[k][j]
import csv
from mpi4py import MPI

FILE = "matrix.csv"     # copy from your chit

comm = MPI.COMM_WORLD
rank = comm.Get_rank()     # my id: 0, 1, 2 ...
size = comm.Get_size()     # total processes started by mpiexec

# ---- master reads A from the CSV and defines B ----
if rank == 0:
    row_ids = []
    A = []
    with open(FILE) as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        for row in reader:
            row_ids.append(row["row_id"].strip())
            A.append([int(row["col_0"]), int(row["col_1"]), int(row["col_2"]), int(row["col_3"])])
    B = [[1, 0, 2, 1],
         [0, 1, 0, 2],
         [1, 1, 1, 0],
         [2, 0, 1, 1]]
    print("Processes:", size, flush=True)
    print("Matrix A:", A, flush=True)
    print("Matrix B:", B, flush=True)
else:
    B = None       # workers do not have B yet

# ---- BROADCAST: everyone gets the full B ----
B = comm.bcast(B, root=0)
if rank == 0:
    print("\nBROADCAST: B sent to all", size, "ranks", flush=True)

# ---- SCATTER: split the rows of A, one piece per rank ----
if rank == 0:
    rows = len(A)
    chunk = (rows + size - 1) // size      # rows per rank, rounded up
    pieces = []
    print("\nSCATTER:", flush=True)
    for r in range(size):
        start = r * chunk
        end = min(start + chunk, rows)
        piece = []
        for i in range(start, end):
            piece.append([i, A[i]])        # [row number, the row]
        pieces.append(piece)
        print("  Rank", r, "gets rows", [p[0] for p in piece], flush=True)
else:
    pieces = None

my_rows = comm.scatter(pieces, root=0)     # each rank receives only its piece

# ---- COMPUTE: each rank multiplies its rows by B ----
my_result = []
for item in my_rows:
    i = item[0]
    a_row = item[1]
    c_row = []
    for j in range(len(B[0])):
        total = 0
        for k in range(len(B)):
            total += a_row[k] * B[k][j]
        c_row.append(total)
    my_result.append([i, c_row])

# ---- GATHER: master collects every rank's rows ----
gathered = comm.gather(my_result, root=0)

if rank == 0:
    C = [None] * len(A)
    print("\nGATHER:", flush=True)
    for r in range(size):
        for item in gathered[r]:
            C[item[0]] = item[1]
            print("  Rank", r, "->", row_ids[item[0]], "=", item[1], flush=True)
    print("\nFinal matrix C = A x B:", flush=True)
    for i in range(len(C)):
        print(" ", row_ids[i], C[i], flush=True)
