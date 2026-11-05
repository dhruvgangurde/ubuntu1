DC LAB CODES - Dhruv Gangurde (2024300061)   all tested, Python standard library only

Folder              Program             CSV              Check your output against
01_cristian         cristian.py         cristian.csv     best client C4, RTT 20 ms
02_berkeley         berkeley.py         berkeley.csv     agreed time 3600.75
03_lamport          lamport.py          lamport.csv      P1=6, P2=3, P3=5
04_vector_clock     vector.py           vector.csv       P1=[2,0,0] P2=[1,2,0] P3=[1,2,2], 7 concurrent pairs
05_bully            bully.py            bully.csv        new coordinator 4, 12 messages
06_ring             ring.py             ring.csv         new coordinator 4, 6 messages
07_load_balancing   lb.py               lb.csv           imbalance 165 (RR) vs 40 (LC)
08_rpc              rpc.py              rpc.csv          4 successful, 1 failed (Method not found)
09_multithreading   multithreading.py   tasks.csv        900 ms sequential, ~330 ms concurrent, race demo 20 vs 100
10_mpi_matrix       mpi_matrix.py       matrix.csv       run: mpiexec -n 3 python mpi_matrix.py   (needs mpi4py)

RUN:  cd 05_bully   then   python bully.py      (Windows: py bully.py)

IN THE EXAM
1. Make the CSV with the exact filename and columns from the chit, 3-5 rows.
2. Change FILE at the top of the program (and INITIATOR / PROCESSES / WORKERS if the chit says so).
3. Run it.

BEFORE YOU RUN
- CSV values are strings: int() only what you do arithmetic on
- RECEIVE row must come AFTER its matching SEND row (Lamport, Vector)
- Vector: PROCESSES order = slot order
- Ring: next_node_id values must form one closed circle
- Berkeley: first CSV row = master
- RPC: change the method bodies in execute() to match the chit
