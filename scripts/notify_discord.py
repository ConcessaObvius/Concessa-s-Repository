import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone
from typing import Any, Dict

import requests

SECRETS_PATH = pathlib.Path(__file__).resolve().parents[1] / ".secrets" / "discord_webhook.json"


def load_webhook_url() -> str:
    if not SECRETS_PATH.exists():
        raise FileNotFoundError(f"Missing webhook secrets file: {SECRETS_PATH}")
    data = json.loads(SECRETS_PATH.read_text())
    url = data.get("url")
    if not url:
        raise ValueError("discord_webhook.json must contain a non-empty 'url'")
    return url


def build_payload(event: str, status: str, message: str) -> Dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat()
    content = f"**{event}** — {status}\n{message}\n`{timestamp}`"
    return {"content": content}


def post_webhook(payload: Dict[str, Any]):
    url = load_webhook_url()
    resp = requests.post(url, json=payload, timeout=15)
    if resp.status_code >= 300:
        raise RuntimeError(f"Discord webhook error {resp.status_code}: {resp.text}")


def main():
    parser = argparse.ArgumentParser(description="Send a Discord webhook notification")
    parser.add_argument("--event", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--message", required=True)
    args = parser.parse_args()

    payload = build_payload(args.event, args.status, args.message)
    try:
        post_webhook(payload)
    except Exception as exc:  # noqa: BLE001
        print(f"Webhook send failed: {exc}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
