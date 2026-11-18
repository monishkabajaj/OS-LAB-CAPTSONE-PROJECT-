from modules.cpu_scheduling import run_cpu_menu
from modules.memory_management import run_memory_menu
from modules.deadlock import run_deadlock_menu
from modules.disk_scheduling import run_disk_menu
from modules.performance import run_comparison
from modules.reporting import log_event, show_recent_logs

MENU = """
========== OSSim: OS Resource Management Simulator ==========
1. CPU Scheduling
2. Memory Management
3. Deadlock Detection (Banker's Algorithm)
4. Disk Scheduling
5. Compare CPU Scheduling Algorithms
6. View Recent Activity Log
0. Exit
"""

def main():
    log_event("Application started")
    while True:
        print(MENU)
        choice = input("Select an option: ").strip()
        try:
            if choice == "1":
                run_cpu_menu()
            elif choice == "2":
                run_memory_menu()
            elif choice == "3":
                run_deadlock_menu()
            elif choice == "4":
                run_disk_menu()
            elif choice == "5":
                run_comparison()
            elif choice == "6":
                show_recent_logs()
            elif choice == "0":
                log_event("Application closed")
                print("Thank you for using OSSim.")
                break
            else:
                print("Invalid choice. Enter a number from 0 to 6.")
        except (ValueError, IndexError) as exc:
            print(f"Input error: {exc}")
            log_event(f"Input error: {exc}")
        except Exception as exc:
            print(f"Unexpected error: {exc}")
            log_event(f"Unexpected error: {exc}")

if __name__ == "__main__":
    main()
