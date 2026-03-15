import argparse
import json
import pathlib
from datetime import datetime, timezone
from typing import Any, Dict

STATE_PATH = pathlib.Path(__file__).resolve().parents[1] / "backups" / "state_index.json"


def load_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"jobs": {}, "history": [], "updated_at": None}


def save_state(state: Dict[str, Any]):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Update automation state index")
    parser.add_argument("--job", required=True)
    parser.add_argument("--status", required=True, choices=["success", "failure", "noop"])
    parser.add_argument("--artifact", default=None)
    parser.add_argument("--notes", default=None)
    parser.add_argument("--history-limit", type=int, default=20)
    args = parser.parse_args()

    state = load_state()
    now = datetime.now(timezone.utc).isoformat()

    job_entry = {
        "job": args.job,
        "last_status": args.status,
        "last_run_utc": now,
        "artifact": args.artifact,
        "notes": args.notes,
    }
    state.setdefault("jobs", {})[args.job] = job_entry

    history_entry = {
        "job": args.job,
        "status": args.status,
        "timestamp": now,
        "artifact": args.artifact,
        "notes": args.notes,
    }
    history = [history_entry] + state.get("history", [])
    state["history"] = history[: args.history_limit]
    state["updated_at"] = now

    save_state(state)
    print(f"Recorded {args.job} ({args.status}) at {now}")


if __name__ == "__main__":
    main()
