"""Career Coach Agent — final markdown report."""
from __future__ import annotations

import json
from typing import Any

from agents.base_agent import BaseAgent


class CoachAgent(BaseAgent):
    name = "coach"
    prompt_file = "coach"

    def build_user_message(self, context: dict[str, Any]) -> str:
        return json.dumps({
            "session_summary": {
                "target_role": context.get("setup", {}).get("target_role"),
                "interview_type": context.get("setup", {}).get("interview_type"),
                "turns_completed": context.get("turn_number", 0),
                "difficulty": context.get("setup", {}).get("difficulty"),
            },
            "strategy": context.get("strategy", {}),
            "all_turn_evaluations": context.get("evaluations", []),
            "full_transcript": context.get("transcript", []),
            "aggregate_scores": context.get("aggregate_scores", {}),
        }, indent=2)

    async def run(self, context: dict[str, Any], *, json_mode: bool = True) -> str:
        return await super().run(context, json_mode=False)  # type: ignore[return-value]

    @property
    def temperature(self) -> float:
        return 0.6
