# OPERATING SYSTEM LAB CAPSTONE PROJECT
**NAME** : **MONISHKA BAJAJ**

**ROLL NO.** : **2401010161**

**PROGRAM** :  **BTECH CSE**

**COURSE** : **OPERATING SYSTEM LAB**

**COURSE CODE** : **ENCS351**

# OS Resource Management Simulator

## Overview
OS Resource Management Simulator is an integrated, menu-driven Python and Bash application that simulates CPU scheduling, memory allocation, deadlock safety, and disk scheduling. It compares algorithms, exports CSV reports, and records activity in a log.

## Requirements
- Python 3.9 or later
- Windows: Python installed; run from PowerShell or VS Code terminal
- Bash integration: Git Bash or WSL on Windows; Bash is available by default on most Linux/macOS systems
- Optional: `pip install -r requirements.txt` for future chart extensions. Core functionality uses only the Python standard library.

## Run
### Windows (PowerShell / CMD)
```powershell
python main.py
```
### Linux / macOS / Git Bash / WSL
```bash
chmod +x scripts/run.sh
./scripts/run.sh
```

## Menu
1. CPU Scheduling: FCFS, non-preemptive SJF, Round Robin
2. Memory Management: First Fit, Best Fit, Worst Fit
3. Deadlock Detection: Banker's safety algorithm
4. Disk Scheduling: FCFS, SSTF, SCAN
5. Compare CPU algorithms using a common workload
6. View activity log
0. Exit

## Sample data
`data/sample_processes.csv` contains four processes. The CPU menu also includes the same built-in dataset for a quick run. The disk and deadlock modules contain documented teaching datasets.

## Outputs
- `reports/*.csv`: generated scheduling, allocation, disk and comparison results
- `logs/activity.log`: timestamped application activity
- `screenshots/`: sample terminal evidence

## Tests
Run:
```bash
python -m unittest discover -s tests -v
```

## Bash scripts
- `scripts/run.sh` launches the Python application.
- `scripts/cleanup.sh` removes generated CSV reports and the activity log but preserves source code.

## Design notes and assumptions
- CPU scheduling uses integer time units. SJF is non-preemptive.
- Round Robin uses a user-supplied positive time quantum.
- Memory blocks are variable-sized holes; each request is allocated once and leftover capacity remains in that block.
- Banker's algorithm checks whether the supplied state has at least one safe completion sequence. The example is a safe state.
- Disk tracks are numbered 0 through 199. SCAN moves toward higher tracks first, reaches the disk end when there are requests in that direction, then reverses.
- This is a simulator, not a kernel or real resource controller. It does not change host operating-system processes, RAM, or disks.

## Troubleshooting
- If `python` is not recognized on Windows, install Python and enable “Add Python to PATH”, or try `py main.py`.
- If permission is denied for the Bash script, run `chmod +x scripts/run.sh`.
- If a module import fails, run the command from the project root (the folder containing `main.py`).
