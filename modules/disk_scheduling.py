from modules.reporting import save_csv, log_event

def disk_schedule(requests, head, algorithm, disk_size=200):
    if not requests or any(r < 0 or r >= disk_size for r in requests):
        raise ValueError(f"Requests must be between 0 and {disk_size-1}.")
    if not 0 <= head < disk_size:
        raise ValueError("Initial head position is outside the disk.")
    if algorithm == "FCFS":
        order = requests[:]
    elif algorithm == "SSTF":
        pending, pos, order = requests[:], head, []
        while pending:
            nxt = min(pending, key=lambda x: abs(x-pos))
            order.append(nxt); pending.remove(nxt); pos = nxt
    elif algorithm == "SCAN":
        lower = sorted([r for r in requests if r < head], reverse=True)
        upper = sorted([r for r in requests if r >= head])
        order = upper + ([disk_size-1] if upper and upper[-1] != disk_size-1 else [])
        order += lower + ([0] if lower and lower[-1] != 0 else [])
    else:
        raise ValueError("Algorithm must be FCFS, SSTF or SCAN.")
    path = [head] + order
    movement = sum(abs(path[i+1]-path[i]) for i in range(len(path)-1))
    return order, movement

def run_disk_menu():
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    print("Sample requests:", requests, "| initial head:", head)
    if input("Use sample data? (y/n): ").strip().lower() == "n":
        requests = [int(x) for x in input("Requests separated by spaces: ").split()]
        head = int(input("Initial head position: "))
    print("1. FCFS  2. SSTF  3. SCAN")
    option = input("Algorithm: ").strip()
    alg = {"1":"FCFS","2":"SSTF","3":"SCAN"}.get(option)
    if not alg: raise ValueError("Invalid disk scheduling algorithm.")
    order, movement = disk_schedule(requests, head, alg)
    print("Service order:", " -> ".join(map(str, order)))
    print("Total head movement:", movement, "tracks")
    save_csv("disk_scheduling.csv", ["Algorithm","Service order","Total head movement"],
             [[alg, " -> ".join(map(str, order)), movement]])
    log_event(f"Disk scheduling executed: {alg}")
