"""Interviewer Agent — conducts adaptive interview."""
from __future__ import annotations

import json
from typing import Any

from agents.base_agent import BaseAgent


class InterviewerAgent(BaseAgent):
    name = "interviewer"
    prompt_file = "interviewer"

    def build_user_message(self, context: dict[str, Any]) -> str:
        history = [
            {"role": m.get("role"), "content": m.get("content")}
            for m in context.get("transcript", [])
        ]
        return json.dumps({
            "strategy": context.get("strategy", {}),
            "turn_number": context.get("turn_number", 1),
            "conversation_history": history,
            "evaluator_feedback": context.get("evaluator_feedback"),
            "candidate_profile": {
                "target_role": context.get("setup", {}).get("target_role"),
                "resume_snippet": context.get("setup", {}).get("resume_snippet", ""),
                "interview_type": context.get("setup", {}).get("interview_type"),
            },
        }, indent=2)

    @property
    def temperature(self) -> float:
        return 0.75
