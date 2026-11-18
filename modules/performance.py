from modules.cpu_scheduling import SAMPLE, fcfs, sjf_non_preemptive, round_robin
from modules.reporting import save_csv, log_event

def run_comparison():
    algorithms = [
        ("FCFS", lambda: fcfs(SAMPLE)),
        ("SJF", lambda: sjf_non_preemptive(SAMPLE)),
        ("Round Robin (q=2)", lambda: round_robin(SAMPLE, 2))
    ]
    rows = []
    print("\\nCPU algorithm comparison (same sample dataset)")
    print(f"{'Algorithm':<20}{'Avg waiting':>15}{'Avg turnaround':>18}")
    for name, fn in algorithms:
        metrics, _ = fn()
        avg_wt = sum(x["waiting"] for x in metrics) / len(metrics)
        avg_tat = sum(x["turnaround"] for x in metrics) / len(metrics)
        rows.append([name, round(avg_wt, 2), round(avg_tat, 2)])
        print(f"{name:<20}{avg_wt:>15.2f}{avg_tat:>18.2f}")
    save_csv("cpu_algorithm_comparison.csv", ["Algorithm","Average waiting time","Average turnaround time"], rows)
    print("\\nObservation: lower averages indicate better results for this dataset; no algorithm is best for every workload.")
    log_event("CPU algorithm comparison completed")
