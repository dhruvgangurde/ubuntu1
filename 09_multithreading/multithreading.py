# MULTITHREADING WITH A MUTEX LOCK
# each thread_name = one worker thread; threads run at the same time
# all threads update the SAME shared data (status table)
# lock.acquire() ... lock.release() -> only one thread in the critical section
# sequential time = sum of all bursts | concurrent time = slowest worker
import csv
import threading
import time

FILE = "tasks.csv"     # copy from your chit
RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}     # lower number = runs first

lock = threading.Lock()      # the mutex
tasks_by_thread = {}         # "Worker_1" -> [[rank, task_id, burst, priority], ...]
status = {}                  # SHARED: task_id -> status
completed = []               # SHARED: [task_id, worker, finish_time]
total_burst = 0

with open(FILE) as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        task_id = row["task_id"].strip()
        name = row["thread_name"].strip()
        burst = int(row["burst_ms"])
        priority = row["priority"].strip().upper()
        status[task_id] = row["status"].strip().upper()
        total_burst += burst
        if name not in tasks_by_thread:
            tasks_by_thread[name] = []
        tasks_by_thread[name].append([RANK[priority], task_id, burst, priority])

# sort each thread's tasks by priority (HIGH first)
for name in tasks_by_thread:
    tasks_by_thread[name].sort()

print("Task allocation:")
for name in tasks_by_thread:
    line = ""
    for t in tasks_by_thread[name]:
        line += t[1] + "(" + t[3] + "," + str(t[2]) + "ms) "
    print(name, ":", line)

start = time.time()
def now():
    return round(time.time() - start, 2)      # seconds since start

# what each thread runs
def worker(name, my_tasks):
    print("[", now(), "s]", name, "started")
    for t in my_tasks:
        task_id = t[1]
        burst = t[2]
        print("[", now(), "s]", name, "processing", task_id, "(", burst, "ms )")
        time.sleep(burst / 1000)          # the work: OUTSIDE the lock, threads overlap

        lock.acquire()                    # ---- critical section starts
        status[task_id] = "COMPLETED"
        completed.append([task_id, name, now()])
        print("[", now(), "s]", name, "marked", task_id, "COMPLETED (holding lock)")
        lock.release()                    # ---- critical section ends
    print("[", now(), "s]", name, "finished")

print("\nExecution log:")
threads = []
for name in tasks_by_thread:
    t = threading.Thread(target=worker, args=(name, tasks_by_thread[name]))
    threads.append(t)
    t.start()              # start running worker(...) in the background

for t in threads:
    t.join()               # main program waits for every thread

elapsed = now()
print("\nCompleted tasks (in completion order):")
for i in range(len(completed)):
    c = completed[i]
    print(i + 1, ".", c[0], "by", c[1], "at", c[2], "s | status =", status[c[0]])

print("\nSequential time:", total_burst, "ms")
print("Concurrent time:", int(elapsed * 1000), "ms using", len(threads), "threads")

# ---------- RACE CONDITION DEMO ----------
# 5 threads each add 1 to a shared counter 20 times -> should be 100

def add_unsafe(counter):
    for i in range(20):
        value = counter[0]         # read
        time.sleep(0.001)          # another thread sneaks in here
        counter[0] = value + 1     # write (can overwrite someone's update)

def add_safe(counter):
    for i in range(20):
        lock.acquire()             # read + write together
        value = counter[0]
        time.sleep(0.001)
        counter[0] = value + 1
        lock.release()

print("\nRace condition demo (expected 100):")
for pair in [["WITHOUT lock", add_unsafe], ["WITH lock", add_safe]]:
    counter = [0]      # a list, so all threads change the same object
    group = []
    for i in range(5):
        t = threading.Thread(target=pair[1], args=(counter,))
        group.append(t)
        t.start()
    for t in group:
        t.join()
    print(pair[0], ": counter =", counter[0])
