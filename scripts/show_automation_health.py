import json
import pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "backups" / "state_index.json"
LOG_DIR = ROOT / "logs" / "automation"


def show_state():
    if not STATE_PATH.exists():
        print("No state_index.json found.")
        return
    state = json.loads(STATE_PATH.read_text())
    print("=== Job Status ===")
    for job, meta in state.get("jobs", {}).items():
        print(f"{job}: {meta.get('last_status')} at {meta.get('last_run_utc')}")
        if meta.get("artifact"):
            print(f"  artifact: {meta['artifact']}")
        if meta.get("notes"):
            print(f"  notes: {meta['notes']}")
    print()
    print("Updated at:", state.get("updated_at"))


def tail_logs(limit: int = 5):
    if not LOG_DIR.exists():
        print("No logs/automation directory.")
        return
    print("=== Log Tail ===")
    for log_path in sorted(LOG_DIR.glob("*.log")):
        print(f"-- {log_path.name} (modified {datetime.fromtimestamp(log_path.stat().st_mtime)})")
        lines = log_path.read_text().splitlines()
        for line in lines[-limit:]:
            print("   ", line)
        print()


def main():
    show_state()
    tail_logs()


if __name__ == "__main__":
    main()
