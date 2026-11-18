import csv
import logging
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(ROOT, "reports")
LOG_DIR = os.path.join(ROOT, "logs")
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "activity.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_event(message):
    logging.info(message)

def save_csv(filename, headers, rows):
    path = os.path.join(REPORT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    log_event(f"Report generated: {filename}")
    print(f"Saved report: {path}")
    return path

def show_recent_logs(limit=12):
    path = os.path.join(LOG_DIR, "activity.log")
    if not os.path.exists(path):
        print("No activity log found.")
        return
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    print("----- Recent activity -----")
    print("".join(lines[-limit:]) or "No activity yet.")
