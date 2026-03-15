import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "backups" / "state_index.json"

if not STATE_PATH.exists():
    print("No automation state recorded yet.")
    raise SystemExit(0)

state = json.loads(STATE_PATH.read_text())
print("Automation Health Summary")
print("Updated:", state.get("updated_at"))
for job, meta in state.get("jobs", {}).items():
    print(f"- {job}: {meta.get('last_status')} at {meta.get('last_run_utc')}")
