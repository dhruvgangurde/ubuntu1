# BERKELEY ALGORITHM
# diff = (node - master) clock
# discard a node if it is faulty OR |clock - median| > THRESHOLD
# average = sum(diff of good nodes) / number of good nodes
# agreed time = master time + average
# adjust = agreed time - node's own clock   (every node gets one, even faulty ones)
import csv, statistics

FILE = "berkeley.csv"    # copy from your chit
THRESHOLD = 60           # clock more than 60 sec from the median = outlier

id = []
clock_time = []
isfaulty = []
with open(FILE) as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        id.append(row['node_id'].strip())
        clock_time.append(int(row['clock_time_sec']))
        isfaulty.append(row['is_faulty'].strip().upper() == "TRUE")
master = id[0]            # first row = master
master_time = clock_time[0]
print("Master:", master, "clock =", master_time)

# step 1: difference of every node from the master
for i in range(len(id)):
    print(id[i], clock_time[i], "diff =", clock_time[i] - master_time)

# step 2: add up the diffs of the good nodes only
median = statistics.median(clock_time)
print("Median =", median)
total = 0
count = 0
for i in range(len(id)):
    if isfaulty[i] == True:
        print(id[i], "discarded (faulty)")
        continue
    if abs(clock_time[i] - median) > THRESHOLD:
        print(id[i], "discarded (far from median)")
        continue
    total += (clock_time[i] - master_time)
    count += 1

# step 3: average and agreed time
if count == 0:
    print("No good clocks to average")
else:
    average = total / count
    agreed = master_time + average
    print("Average =", average, "| Agreed time =", agreed)

    # step 4: adjustment for every node
    for i in range(len(id)):
        adjust = agreed - clock_time[i]
        new_time = clock_time[i] + adjust
        print(id[i], "old =", clock_time[i], "| adjust by", adjust, "| new =", new_time)
        clock_time[i] = new_time
