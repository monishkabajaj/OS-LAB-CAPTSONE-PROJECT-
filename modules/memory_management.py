from modules.reporting import save_csv, log_event

def allocate(blocks, requests, strategy):
    if any(int(x) <= 0 for x in blocks + requests):
        raise ValueError("Memory block sizes and requests must be positive.")
    free = [int(x) for x in blocks]
    results = []
    for idx, size in enumerate(requests, 1):
        candidates = [i for i, b in enumerate(free) if b >= size]
        chosen = None
        if candidates:
            if strategy == "First Fit": chosen = candidates[0]
            elif strategy == "Best Fit": chosen = min(candidates, key=lambda i: free[i])
            elif strategy == "Worst Fit": chosen = max(candidates, key=lambda i: free[i])
            else: raise ValueError("Unknown allocation strategy.")
            free[chosen] -= size
        results.append([f"R{idx}", size, f"B{chosen+1}" if chosen is not None else "Not allocated",
                        free[chosen] if chosen is not None else "—"])
    return results, free

def run_memory_menu():
    blocks = [100, 500, 200, 300, 600]
    requests = [212, 417, 112, 426]
    print("Default blocks:", blocks, "| requests:", requests)
    if input("Use sample data? (y/n): ").strip().lower() == "n":
        blocks = [int(x) for x in input("Enter block sizes separated by spaces: ").split()]
        requests = [int(x) for x in input("Enter request sizes separated by spaces: ").split()]
    print("1. First Fit  2. Best Fit  3. Worst Fit")
    option = input("Strategy: ").strip()
    strategy = {"1":"First Fit","2":"Best Fit","3":"Worst Fit"}.get(option)
    if not strategy: raise ValueError("Invalid memory strategy.")
    rows, free = allocate(blocks, requests, strategy)
    print(f"\\n{strategy} allocation")
    print(f"{'Request':<10}{'Size':<10}{'Block':<16}{'Remaining':<10}")
    for row in rows: print(f"{row[0]:<10}{row[1]:<10}{row[2]:<16}{row[3]}")
    print("Remaining block capacities:", free)
    save_csv("memory_allocation.csv", ["Request","Size","Block","Remaining capacity"], rows)
    log_event(f"Memory allocation executed: {strategy}")
