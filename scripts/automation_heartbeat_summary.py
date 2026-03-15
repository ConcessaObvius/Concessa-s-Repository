import json
import pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "backups" / "state_index.json"
LOG_DIR = ROOT / "logs" / "automation"
JOB_LOGS = {
    "nightly_backup": "nightly_backup.log",
    "git_status_push": "git_status_push.log",
}


def load_state():
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text())


def tail_log(log_name: str, limit: int = 2):
    log_path = LOG_DIR / log_name
    if not log_path.exists():
        return "log missing"
    lines = log_path.read_text().splitlines()
    snippet = " | ".join(lines[-limit:]) if lines else "(empty)"
    mtime = datetime.fromtimestamp(log_path.stat().st_mtime).isoformat()
    return f"{snippet} (updated {mtime})"


def main():
    state = load_state()
    jobs = state.get("jobs", {})
    if not jobs:
        print("No automation jobs recorded yet.")
        return
    for job in sorted(jobs):
        meta = jobs[job]
        status = meta.get("last_status")
        timestamp = meta.get("last_run_utc")
        notes = meta.get("notes")
        artifact = meta.get("artifact")
        line = f"{job}: {status} at {timestamp}"
        if notes:
            line += f" | notes: {notes}"
        if artifact:
            line += f" | artifact: {artifact}"
        print(line)
        log_name = JOB_LOGS.get(job)
        if log_name:
            print("  tail:", tail_log(log_name))
    print("State updated at:", state.get("updated_at"))


if __name__ == "__main__":
    main()
