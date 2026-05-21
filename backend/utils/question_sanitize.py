"""Ensure interviewer output is conversational text, not raw JSON."""
from __future__ import annotations

import json
import re
from typing import Any


def is_json_blob(text: str) -> bool:
    t = text.strip()
    if not t.startswith("{"):
        return False
    try:
        json.loads(t)
        return True
    except json.JSONDecodeError:
        return bool(re.match(r"^\s*\{[\s\S]*\}\s*$", t))


def fallback_question(strategy: dict[str, Any] | None, turn: int = 1) -> str:
    if strategy:
        hint = strategy.get("opening_question_hint")
        if hint and isinstance(hint, str):
            return (
                f"Thanks for being here today. To begin — {hint.lower() if hint[0].isupper() else hint}: "
                "what draws you to this role, and what would success look like in your first few months?"
            )
    defaults = [
        "Thanks for joining today. To start — what draws you to this role, and what would success look like in your first six months?",
        "Tell me about a recent project you're proud of. What was your specific contribution?",
        "Walk me through a challenging situation at work and how you handled it.",
    ]
    return defaults[min(turn - 1, len(defaults) - 1)]


def normalize_interviewer_reply(
    raw: str,
    strategy: dict[str, Any] | None = None,
    turn: int = 1,
) -> str:
    text = (raw or "").strip()
    if not text or is_json_blob(text):
        return fallback_question(strategy, turn)
    # Strip accidental markdown code fences
    if text.startswith("```"):
        text = re.sub(r"^```\w*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
        if is_json_blob(text):
            return fallback_question(strategy, turn)
    return text
