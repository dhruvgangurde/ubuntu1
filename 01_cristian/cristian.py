# CRISTIAN'S ALGORITHM
# rtt = t1 - t0
# server time now = t_server + rtt / 2
# offset = server time - t1  # t1 is client's own clock
# offset > 0 -> client BEHIND (move forward) | offset < 0 -> client AHEAD (slow down)
# new client time = server time now
# accuracy = +/- rtt / 2
# most accurate client = smallest rtt
import csv

FILE = "cristian.csv"    # copy from your chit

best_rtt = None    # smallest rtt seen so far
best_client = ""   # client that had it

with open(FILE) as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        client = row['client_id']
        t0 = int(row['t0_send_ms'])
        ts = int(row['t_server_ms'])
        t1 = int(row['t1_recv_ms'])
        rtt = t1 - t0
        server_time = ts + rtt / 2
        offset = server_time - t1
        accuracy = rtt / 2
        client_time = server_time   # client sets its clock to the estimated server time

        print(client)
        print("  T0 (client sent request)    :", t0)
        print("  Ts (server's clock reading) :", ts)
        print("  T1 (client got the reply)   :", t1)
        print("  RTT = T1 - T0               :", rtt)
        print("  Server time now = Ts+RTT/2  :", server_time)
        print("  Offset = server time - T1   :", offset)
        if offset > 0:
            print("  Behind by", offset, "-> move clock forward")
        elif offset == 0:
            print("  In sync")
        else:
            print("  Ahead by", -offset, "-> slow clock down")
        print("  New client time             :", client_time)
        print("  Accuracy                    : +/-", accuracy)

        # keep the client with the smallest rtt
        if best_rtt is None or rtt < best_rtt:
            best_rtt = rtt
            best_client = client

# after the loop (outside the with block)
print("Most accurate client:", best_client, "with RTT", best_rtt, "ms")
