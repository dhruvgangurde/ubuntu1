# VECTOR CLOCKS (one counter per process, slot order = PROCESSES)
# INTERNAL : my slot + 1
# SEND     : my slot + 1, attach a COPY of my vector to the message
# RECEIVE  : each slot = max(my value, message value), then my slot + 1
# A BEFORE B : every slot of A <= B and at least one smaller
# otherwise  : CONCURRENT
import csv

FILE = "vector.csv"                # copy from your chit
PROCESSES = ["P1", "P2", "P3"]     # slot order of [V1, V2, V3]
n = len(PROCESSES)

clocks = {}     # process -> its vector, e.g. {"P1": [0, 0, 0]}
mailbox = {}    # receiver -> list of vectors waiting for it
for p in PROCESSES:
    clocks[p] = [0] * n
    mailbox[p] = []

events = []     # [event, vector] saved for the pair comparison

with open(FILE) as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        event = row["event_id"].strip()
        process = row["process_id"].strip()
        action = row["event_action"].strip().upper()
        target = row["target_process"].strip()

        me = PROCESSES.index(process)     # which slot is mine

        if action == "INTERNAL":
            clocks[process][me] += 1
            print(event, process, "INTERNAL ->", clocks[process])

        elif action == "SEND":
            clocks[process][me] += 1
            # .copy() = snapshot, the original list keeps changing later
            mailbox[target].append(clocks[process].copy())
            print(event, process, "SEND to", target, "->", clocks[process])

        elif action == "RECEIVE":
            msg = mailbox[process].pop(0)
            before = clocks[process].copy()
            for k in range(n):
                clocks[process][k] = max(clocks[process][k], msg[k])
            clocks[process][me] += 1
            print(event, process, "RECEIVE | max(", before, ",", msg, ") then +1 ->", clocks[process])

        events.append([event, clocks[process].copy()])

print("\nFinal vectors:")
for p in PROCESSES:
    print(p, "=", clocks[p])

# compare two vectors: BEFORE / AFTER / CONCURRENT
def compare(a, b):
    a_smaller = False    # found a slot where a < b
    b_smaller = False    # found a slot where b < a
    for k in range(len(a)):
        if a[k] < b[k]:
            a_smaller = True
        if b[k] < a[k]:
            b_smaller = True
    if a_smaller and not b_smaller:
        return "BEFORE"
    if b_smaller and not a_smaller:
        return "AFTER"
    return "CONCURRENT"

print("\nCausality of every pair:")
concurrent = 0
for i in range(len(events)):
    for j in range(i + 1, len(events)):    # j after i, so no pair repeats
        e1 = events[i][0]
        v1 = events[i][1]
        e2 = events[j][0]
        v2 = events[j][1]
        result = compare(v1, v2)
        if result == "BEFORE":
            print(e1, v1, "->", e2, v2, ":", e1, "happened before", e2)
        elif result == "AFTER":
            print(e2, v2, "->", e1, v1, ":", e2, "happened before", e1)
        else:
            print(e1, v1, "||", e2, v2, ":", "concurrent")
            concurrent += 1

print("\nConcurrent pairs:", concurrent)
