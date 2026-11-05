# RING ALGORITHM (leader election)
# nodes talk only to their NEXT neighbour; dead nodes are skipped
# phase 1: ELECTION token goes round once, every active node adds its id
# phase 2: leader = max(token); COORDINATOR message goes round once
# messages = 2 x number of active nodes
import csv

FILE = "ring.csv"     # copy from your chit
INITIATOR = 1         # node that notices the failure (from your chit)

nodes = []
next_of = {}     # node -> next node in the ring
active = {}      # node -> True / False
rank = {}        # node -> priority_rank

with open(FILE) as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        node = int(row["node_id"])
        nodes.append(node)
        next_of[node] = int(row["next_node_id"])
        active[node] = row["is_active"].strip().upper() == "TRUE"
        rank[node] = int(row["priority_rank"])

old_leader = max(nodes)     # before the failure, the highest id was coordinator

# next ACTIVE node after 'node' (skip the dead ones)
def next_active(node):
    nxt = next_of[node]
    while active[nxt] == False:
        print("  node", nxt, "is down, skipped")
        nxt = next_of[nxt]
    return nxt

if active[old_leader] == True:
    print("Coordinator", old_leader, "is active. No election needed.")
else:
    print("Node", INITIATOR, "finds coordinator", old_leader, "down. Ring election starts.")

    # phase 1: election token
    print("\nPHASE 1: ELECTION token")
    token = [INITIATOR]
    messages = 0
    current = INITIATOR
    while True:
        nxt = next_active(current)
        print("ELECTION", current, "->", nxt, "| token =", token)
        messages += 1
        if nxt == INITIATOR:
            print("token is back at the initiator")
            break
        token.append(nxt)
        current = nxt

    leader = max(token)
    print("Active ids =", token, "| leader = max =", leader)

    # phase 2: coordinator message
    print("\nPHASE 2: COORDINATOR message")
    current = INITIATOR
    while True:
        nxt = next_active(current)
        print("COORDINATOR", current, "->", nxt, "| new leader =", leader)
        messages += 1
        if nxt == INITIATOR:
            break
        current = nxt

    print("\nOld coordinator:", old_leader)
    print("New coordinator:", leader, "(priority", rank[leader], ")")
    print("Total messages:", messages, "= 2 x", len(token))
