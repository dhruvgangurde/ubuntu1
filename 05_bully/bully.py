# Bully rule: the highest alive node becomes the coordinator
#   ELECTION    -> sent to every node with a bigger id
#   OK          -> a bigger alive node replies, sender steps down
#   COORDINATOR -> winner tells all other alive nodes
import csv

FILE = "bully.csv"    # copy from your chit
INITIATOR = 2         # node that notices the failure (from your chit)

nodes = []        # all node ids
alive = {}        # node -> True / False
old_leader = 0    # current coordinator

with open(FILE) as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        node = int(row["node_id"])
        nodes.append(node)
        alive[node] = row["is_alive"].strip().upper() == "TRUE"
        if row["is_current_coordinator"].strip().upper() == "TRUE":
            old_leader = node

nodes.sort()

if alive[old_leader] == True:
    print("Coordinator", old_leader, "is alive. No election needed.")
else:
    print("Node", INITIATOR, "found that coordinator", old_leader, "is down. Election starts.")
    messages = 0
    leader = 0

    # every alive node from the initiator upwards holds an election
    for current in nodes:
        if current < INITIATOR or alive[current] == False:
            continue
        print("\nNode", current, "holds an election")
        got_ok = False
        for higher in nodes:
            if higher > current:
                print("  ELECTION", current, "->", higher)
                messages += 1
                if alive[higher] == True:
                    print("  OK      ", higher, "->", current)
                    messages += 1
                    got_ok = True
                else:
                    print("  node", higher, "is down, no reply")
        if got_ok == False:
            leader = current
            print("  No OK received -> Node", current, "WINS")

    # winner tells everyone else
    print()
    for node in nodes:
        if alive[node] == True and node != leader:
            print("COORDINATOR", leader, "->", node)
            messages += 1

    print("\nOld coordinator:", old_leader)
    print("New coordinator:", leader)
    print("Total messages:", messages)
