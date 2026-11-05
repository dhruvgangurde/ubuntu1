# RPC / RMI SIMULATION
# client calls a remote method like a local one:
#   client stub : MARSHAL (pack) method + argument into a message
#   network     : carries the message to the server
#   server stub : UNMARSHAL (unpack), look the method up in the registry,
#                 run it, MARSHAL the result and send it back
#   client stub : UNMARSHAL the reply
# a method not in the registry -> "Method not found" error
import csv
import json

FILE = "rpc.csv"     # copy from your chit

# ------------- SERVER SIDE -------------
REGISTRY = ["processData", "assignSubtask", "estimateTokens", "checkQuota"]

# the actual remote procedures (change these to match your chit)
def execute(method, value):
    if method == "processData":
        return value * 2
    elif method == "assignSubtask":
        return "agent-node-" + str(value % 5 + 1)
    elif method == "estimateTokens":
        return value * 4 // 3
    elif method == "checkQuota":
        if value <= 1000:
            return "ALLOWED"
        else:
            return "REJECTED"

def server_stub(request_text):
    request = json.loads(request_text)                       # unmarshal
    method = request["method"]
    value = request["param"]
    print("  [SERVER] unmarshalled:", method, "(", value, ")")

    if method not in REGISTRY:                               # lookup
        print("  [SERVER] method not registered")
        reply = {"call_id": request["call_id"], "status": "ERROR", "result": "Method not found"}
    else:
        result = execute(method, value)                      # run it
        print("  [SERVER] executed:", method, "(", value, ") =", result)
        reply = {"call_id": request["call_id"], "status": "OK", "result": result}

    return json.dumps(reply)                                 # marshal the reply

# ------------- CLIENT SIDE -------------
def client_stub(call_id, client, method, value):
    request = {"call_id": call_id, "client": client, "method": method, "param": value}
    request_text = json.dumps(request)                       # marshal
    print("  [CLIENT] marshalled:", request_text)
    print("  [NETWORK]", len(request_text), "bytes sent to the server")

    reply_text = server_stub(request_text)                   # 'send' to the server

    print("  [NETWORK]", len(reply_text), "bytes returned")
    return json.loads(reply_text)                            # unmarshal the reply

# ------------- MAIN -------------
ok = 0
failed = 0
with open(FILE) as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        call_id = row["call_id"].strip()
        client = row["client_name"].strip()
        method = row["method_name"].strip()
        value = int(row["param_value"])
        stamp = row["timestamp"].strip()

        print("\nCALL", call_id, "at", stamp, ":", client, "->", method, "(", value, ")")
        reply = client_stub(call_id, client, method, value)

        if reply["status"] == "OK":
            print("  [RESULT]", client, "received", reply["result"])
            ok += 1
        else:
            print("  [ERROR]", client, "received", reply["result"])
            failed += 1

print("\nTotal calls:", ok + failed, "| successful:", ok, "| failed:", failed)
