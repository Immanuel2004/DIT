# utils/usage_tracker.py

import os
import json
import datetime

USAGE_LOG_PATH = "logs/usage_log.json"

def log_usage(user_id: str, model: str, tokens_input: int, tokens_output: int, cost: float):
    """Log a single API usage entry for a user."""
    timestamp = datetime.datetime.now().isoformat()

    entry = {
        "user_id": user_id,
        "model": model,
        "timestamp": timestamp,
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "total_tokens": tokens_input + tokens_output,
        "cost": round(cost, 4)
    }

    if os.path.exists(USAGE_LOG_PATH):
        with open(USAGE_LOG_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)
    os.makedirs(os.path.dirname(USAGE_LOG_PATH), exist_ok=True)
    with open(USAGE_LOG_PATH, "w") as f:
        json.dump(data, f, indent=4)

def get_user_summary(user_id: str):
    """Return total cost and tokens used by a user."""
    if not os.path.exists(USAGE_LOG_PATH):
        return {"total_tokens": 0, "total_cost": 0.0}

    with open(USAGE_LOG_PATH, "r") as f:
        data = json.load(f)

    user_entries = [d for d in data if d["user_id"] == user_id]
    total_tokens = sum(d["total_tokens"] for d in user_entries)
    total_cost = sum(d["cost"] for d in user_entries)

    return {
        "total_tokens": total_tokens,
        "total_cost": round(total_cost, 4),
        "entries": user_entries
    }




