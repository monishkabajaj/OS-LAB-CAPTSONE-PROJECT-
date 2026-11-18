from modules.reporting import log_event

def bankers_safety(available, allocation, maximum):
    if len(allocation) != len(maximum):
        raise ValueError("Allocation and maximum matrices must have equal row counts.")
    if any(len(a) != len(available) for a in allocation + maximum):
        raise ValueError("Matrix column count must match available resources.")
    if any(x < 0 for x in available):
        raise ValueError("Available resources cannot be negative.")
    need = [[maximum[i][j] - allocation[i][j] for j in range(len(available))]
            for i in range(len(allocation))]
    if any(x < 0 for row in need for x in row):
        raise ValueError("Allocation cannot exceed maximum demand.")
    work = available[:]
    finish = [False] * len(allocation)
    sequence = []
    changed = True
    while changed:
        changed = False
        for i in range(len(allocation)):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                work = [work[j] + allocation[i][j] for j in range(len(work))]
                finish[i] = True
                sequence.append(f"P{i}")
                changed = True
    return all(finish), sequence, need

def run_deadlock_menu():
    # Canonical safe-state example: 5 processes, 3 resource types.
    available = [3, 3, 2]
    allocation = [[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]
    maximum = [[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]
    safe, sequence, need = bankers_safety(available, allocation, maximum)
    print("Available resources:", available)
    print("Need matrix:")
    for i, row in enumerate(need): print(f"P{i}: {row}")
    if safe: print("System is in a SAFE state. Sequence:", " -> ".join(sequence))
    else: print("System is UNSAFE. No complete safe sequence was found.")
    log_event("Banker's safety check executed")

