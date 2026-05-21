"""Strategist Agent — plans interview strategy."""
from __future__ import annotations

import json
from typing import Any

from agents.base_agent import BaseAgent


class StrategistAgent(BaseAgent):
    name = "strategist"
    prompt_file = "strategist"

    def build_user_message(self, context: dict[str, Any]) -> str:
        setup = context["setup"]
        return json.dumps({
            "target_role": setup["target_role"],
            "resume_snippet": setup.get("resume_snippet", ""),
            "interview_type": setup.get("interview_type", "mixed"),
            "difficulty": setup.get("difficulty", "adaptive"),
            "experience_level": setup.get("experience_level", "mid"),
        }, indent=2)

    @property
    def temperature(self) -> float:
        return 0.5
