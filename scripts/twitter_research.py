import json
import pathlib
import time
from typing import List, Dict

import requests

BASE = "https://api.twitter.com/2"
SECRETS_PATH = pathlib.Path(__file__).resolve().parents[1] / ".secrets" / "twitter_api.json"

with SECRETS_PATH.open() as f:
    CREDS = json.load(f)

HEADERS = {"Authorization": f"Bearer {CREDS['bearer_token']}"}


def twitter_get(path: str, params: Dict[str, str]):
    url = f"{BASE}{path}"
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Twitter API error {resp.status_code}: {resp.text}")
    return resp.json()


def get_user_id(username: str) -> str:
    data = twitter_get(f"/users/by/username/{username}", {"user.fields": "public_metrics,description"})
    return data["data"], data.get("includes", {})


def get_user_tweets(user_id: str, max_results: int = 100) -> List[Dict]:
    tweets: List[Dict] = []
    params = {
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,entities,context_annotations",
        "expansions": "author_id"
    }
    next_token = None
    remaining = max_results
    while remaining > 0:
        if next_token:
            params["pagination_token"] = next_token
        resp = twitter_get(f"/users/{user_id}/tweets", params)
        batch = resp.get("data", [])
        tweets.extend(batch)
        meta = resp.get("meta", {})
        next_token = meta.get("next_token")
        remaining -= len(batch)
        if not next_token or not batch:
            break
        time.sleep(1)  # avoid rate limits
    return tweets


def search_recent(query: str, max_results: int = 50) -> List[Dict]:
    tweets: List[Dict] = []
    params = {
        "query": query,
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,entities",
    }
    next_token = None
    remaining = max_results
    while remaining > 0:
        if next_token:
            params["next_token"] = next_token
        resp = twitter_get("/tweets/search/recent", params)
        batch = resp.get("data", [])
        tweets.extend(batch)
        meta = resp.get("meta", {})
        next_token = meta.get("next_token")
        remaining -= len(batch)
        if not next_token or not batch:
            break
        time.sleep(1)
    return tweets


def summarize_tweets(tweets: List[Dict]) -> List[Dict]:
    summary = []
    for t in tweets:
        metrics = t.get("public_metrics", {})
        text = t.get("text", "").replace("\n", " ")
        summary.append({
            "id": t.get("id"),
            "created_at": t.get("created_at"),
            "like_count": metrics.get("like_count", 0),
            "retweet_count": metrics.get("retweet_count", 0),
            "reply_count": metrics.get("reply_count", 0),
            "quote_count": metrics.get("quote_count", 0),
            "text": text[:280]
        })
    summary.sort(key=lambda x: (x["like_count"], x["retweet_count"]), reverse=True)
    return summary


def main():
    targets = {
        "tiktok_shop_guides": "\"TikTok Shop\" (guide OR playbook OR pdf OR checklist) lang:en -is:retweet",
        "ugc_script_templates": "UGC (script OR template OR prompt) lang:en -is:retweet",
        "ai_marketing_agents": "\"AI agent\" (marketing OR funnel OR ecommerce) lang:en -is:retweet"
    }

    results = {}
    for key, query in targets.items():
        tweets = search_recent(query, max_results=60)
        results[key] = summarize_tweets(tweets)[:15]

    # Felix account snapshot
    felix_user, _ = get_user_id("FelixCraftAI")
    felix_tweets = summarize_tweets(get_user_tweets(felix_user["id"], max_results=80))[:20]

    output = {
        "targets": results,
        "felix": {
            "profile": felix_user,
            "top_tweets": felix_tweets
        }
    }

    out_path = pathlib.Path("analysis/twitter_research.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
