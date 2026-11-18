from modules.reporting import save_csv, log_event

SAMPLE = [
    {"pid": "P1", "arrival": 0, "burst": 7},
    {"pid": "P2", "arrival": 2, "burst": 4},
    {"pid": "P3", "arrival": 4, "burst": 1},
    {"pid": "P4", "arrival": 5, "burst": 4},
]

def validate_processes(processes):
    if not processes:
        raise ValueError("At least one process is required.")
    seen = set()
    for p in processes:
        if not p["pid"] or p["pid"] in seen:
            raise ValueError("Process IDs must be non-empty and unique.")
        seen.add(p["pid"])
        if int(p["arrival"]) < 0 or int(p["burst"]) <= 0:
            raise ValueError("Arrival time must be >= 0 and burst time must be > 0.")

def calculate_metrics(rows):
    result = []
    for p in rows:
        turnaround = p["completion"] - p["arrival"]
        waiting = turnaround - p["burst"]
        response = p["first_start"] - p["arrival"]
        result.append({
            "pid": p["pid"], "arrival": p["arrival"], "burst": p["burst"],
            "completion": p["completion"], "turnaround": turnaround,
            "waiting": waiting, "response": response
        })
    return result

def fcfs(processes):
    validate_processes(processes)
    clock, schedule, completed = 0, [], []
    for p in sorted(processes, key=lambda x: (int(x["arrival"]), x["pid"])):
        start = max(clock, int(p["arrival"]))
        end = start + int(p["burst"])
        schedule.append((p["pid"], start, end))
        completed.append({**p, "arrival": int(p["arrival"]), "burst": int(p["burst"]),
                          "first_start": start, "completion": end})
        clock = end
    return calculate_metrics(completed), schedule

def sjf_non_preemptive(processes):
    validate_processes(processes)
    pending = [dict(p, arrival=int(p["arrival"]), burst=int(p["burst"])) for p in processes]
    clock, completed, schedule = 0, [], []
    while pending:
        ready = [p for p in pending if p["arrival"] <= clock]
        if not ready:
            clock = min(p["arrival"] for p in pending)
            ready = [p for p in pending if p["arrival"] <= clock]
        p = min(ready, key=lambda x: (x["burst"], x["arrival"], x["pid"]))
        pending.remove(p)
        start, end = clock, clock + p["burst"]
        schedule.append((p["pid"], start, end))
        completed.append({**p, "first_start": start, "completion": end})
        clock = end
    return calculate_metrics(completed), schedule

def round_robin(processes, quantum=2):
    validate_processes(processes)
    if quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")
    pending = sorted(
        [dict(p, arrival=int(p["arrival"]), burst=int(p["burst"])) for p in processes],
        key=lambda x: (x["arrival"], x["pid"])
    )
    remaining = {p["pid"]: p["burst"] for p in pending}
    first, completion, schedule = {}, {}, []
    ready, i, clock = [], 0, 0
    while i < len(pending) or ready:
        if not ready and i < len(pending) and clock < pending[i]["arrival"]:
            clock = pending[i]["arrival"]
        while i < len(pending) and pending[i]["arrival"] <= clock:
            ready.append(pending[i]); i += 1
        p = ready.pop(0)
        first.setdefault(p["pid"], clock)
        run = min(quantum, remaining[p["pid"]])
        start, end = clock, clock + run
        schedule.append((p["pid"], start, end))
        clock = end
        remaining[p["pid"]] -= run
        while i < len(pending) and pending[i]["arrival"] <= clock:
            ready.append(pending[i]); i += 1
        if remaining[p["pid"]] > 0:
            ready.append(p)
        else:
            completion[p["pid"]] = clock
    completed = []
    for p in pending:
        completed.append({**p, "first_start": first[p["pid"]], "completion": completion[p["pid"]]})
    return calculate_metrics(completed), schedule

def print_result(name, metrics, schedule):
    print(f"\\n{name} results")
    print("Gantt trace:", " | ".join(f"{pid}[{start}-{end}]" for pid, start, end in schedule))
    print(f"{'PID':<6}{'CT':>6}{'TAT':>7}{'WT':>7}{'RT':>7}")
    for r in sorted(metrics, key=lambda x: x["pid"]):
        print(f"{r['pid']:<6}{r['completion']:>6}{r['turnaround']:>7}{r['waiting']:>7}{r['response']:>7}")
    print(f"Average waiting time: {sum(x['waiting'] for x in metrics)/len(metrics):.2f}")
    print(f"Average turnaround time: {sum(x['turnaround'] for x in metrics)/len(metrics):.2f}")
    save_csv(f"{name.lower().replace(' ', '_')}_results.csv",
             ["PID","Arrival","Burst","Completion","Turnaround","Waiting","Response"],
             [[r["pid"],r["arrival"],r["burst"],r["completion"],r["turnaround"],r["waiting"],r["response"]] for r in metrics])
    log_event(f"CPU scheduling executed: {name}")

def run_cpu_menu():
    print("Use sample processes? (y/n)")
    choice = input("> ").strip().lower()
    if choice == "y":
        processes = SAMPLE
    elif choice == "n":
        count = int(input("Number of processes: "))
        if count <= 0: raise ValueError("Number of processes must be positive.")
        processes = []
        for i in range(count):
            print(f"Process {i+1}")
            processes.append({"pid": input("PID: ").strip(),
                               "arrival": int(input("Arrival time: ")),
                               "burst": int(input("Burst time: "))})
    else:
        raise ValueError("Enter y or n.")
    print("1. FCFS  2. SJF (non-preemptive)  3. Round Robin")
    alg = input("Algorithm: ").strip()
    if alg == "1": name, result = "FCFS", fcfs(processes)
    elif alg == "2": name, result = "SJF", sjf_non_preemptive(processes)
    elif alg == "3":
        q = int(input("Time quantum: "))
        name, result = "Round Robin", round_robin(processes, q)
    else: raise ValueError("Unknown scheduling algorithm.")
    print_result(name, *result)
