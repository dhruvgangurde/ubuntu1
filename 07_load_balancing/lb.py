# ROUND ROBIN       : next worker in rotation (ignores job size)
# LEAST CONNECTIONS : give the job to the worker with the smallest load so far
# imbalance = max load - min load
import csv

FILE = "lb.csv"    # copy from your chit
WORKERS = ["Agent_N1", "Agent_N2", "Agent_N3"]

jobs = []    # each job is [job_id, units]
with open(FILE) as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        jobs.append([row["job_id"].strip(), int(row["compute_units"])])

def balance(strategy):
    load = {}     # worker -> total units
    count = {}    # worker -> number of jobs
    for w in WORKERS:
        load[w] = 0
        count[w] = 0
    index = 0     # rotation position (round robin)

    print("\n--- ", strategy, " ---")
    for job in jobs:
        if strategy == "ROUND ROBIN":
            worker = WORKERS[index % len(WORKERS)]
            index += 1
        else:
            worker = WORKERS[0]
            for w in WORKERS:
                if load[w] < load[worker]:
                    worker = w
        load[worker] += job[1]
        count[worker] += 1
        print(job[0], "(", job[1], "units ) ->", worker)

    for w in WORKERS:
        print(w, ":", count[w], "jobs,", load[w], "units")
    gap = max(load.values()) - min(load.values())
    print("Imbalance =", gap)
    return gap

rr = balance("ROUND ROBIN")
lc = balance("LEAST CONNECTIONS")

print()
if lc < rr:
    print("Least Connections balanced better")
elif rr < lc:
    print("Round Robin balanced better")
else:
    print("Both gave the same balance")
