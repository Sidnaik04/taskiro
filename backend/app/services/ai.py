from google import genai
import json
import re
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables")


_client = genai.Client(api_key=GEMINI_API_KEY)  # reads GEMINI_API_KEY

_MODEL = "gemini-1.5-flash"


def _extract_first_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


def prioritize(tasks: list[dict]) -> dict:
    """
    Input `tasks` as list of dicts with id, title, description, deadline (ISO).
    Output: {"ordered_ids": [ids...], "priorities": {"<id>": "HIGH|MEDIUM|LOW"}}
    """

    now_iso = datetime.now(timezone.utc).isoformat()
    sys_prompt = (
        "You are a helpful planner that prioritizes tasks by deadline proximity. "
        "Earlier deadlines => higher priority. If same day, longer descriptions are slightly higher priority. "
        "Always return strict JSON with keys 'ordered_ids' (array of ids) and 'priorities' (map of id->HIGH|MEDIUM|LOW)."
    )
    user_payload = {"now_utc": now_iso, "tasks": tasks}
    resp = _client.models.generate_content(
        model=_MODEL,
        contents=[{"role": "user", "parts": [sys_prompt, json.dumps(user_payload)]}],
    )

    data = _extract_first_json(resp.text or "")
    # graceful fallback (sort by soonest deadline) if model response missing
    if not data.get("ordered_ids"):
        ordered = sorted(tasks, key=lambda t: t.get("deadline", "9999"))
        data = {
            "ordered_ids": [t["id"] for t in ordered],
            "priorities": {
                t["id"]: (
                    "HIGH"
                    if i < max(1, len(ordered) // 3)
                    else "MEDIUM" if i < max(2, 2 * len(ordered) // 3) else "LOW"
                )
                for i, t in enumerate(ordered)
            },
        }

    return data
