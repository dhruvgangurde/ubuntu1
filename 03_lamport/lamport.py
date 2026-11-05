# INTERNAL : L = L + 1
# SEND     : L = L + 1, message carries T = L
# RECEIVE  : L = max(L, T) + 1
import csv

FILE = "lamport.csv"    # copy from your chit

clocks = {}     # current clock of each process, e.g. {"P1": 2}
mailbox = {}    # messages in transit, e.g. {"P2": [1]}  (key = receiver)
order = []      # [clock, process, event] for the final sort

with open(FILE) as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        event = row["event_id"].strip()
        process = row["process_id"].strip()
        kind = row["event_type"].strip().upper()
        target = row["message_to"].strip()
        start = int(row["initial_clock"])

        # first time we see a process, its clock starts at initial_clock
        if process not in clocks:
            clocks[process] = start

        old = clocks[process]

        if kind == "INTERNAL":
            clocks[process] = old + 1
            print(event, process, "INTERNAL | L =", old, "+ 1 =", clocks[process])

        elif kind == "SEND":
            clocks[process] = old + 1
            # put the message (its timestamp) in the receiver's mailbox
            if target not in mailbox:
                mailbox[target] = []
            mailbox[target].append(clocks[process])
            print(event, process, "SEND to", target, "| L =", old, "+ 1 =", clocks[process], "| message T =", clocks[process])

        elif kind == "RECEIVE":
            t = mailbox[process].pop(0)     # oldest waiting message
            clocks[process] = max(old, t) + 1
            print(event, process, "RECEIVE | L = max(", old, ",", t, ") + 1 =", clocks[process])

        order.append([clocks[process], process, event])

print("\nFinal clocks:")
for p in clocks:
    print(p, "=", clocks[p])

# sort by clock, ties broken by process id -> total order
order.sort()
print("\nTotal order:")
for item in order:
    print(item[2], "(", item[1], ", L =", item[0], ")")
