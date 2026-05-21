import json
from typing import Any

from backend.agents.base import BaseAgent


class StrategistAgent(BaseAgent):
    name = "strategist"
    prompt_name = "strategist"

    def build_user_message(self, ctx: dict[str, Any]) -> str:
        setup = ctx["setup"]
        return json.dumps({
            "target_role": setup["target_role"],
            "background": setup.get("background", ""),
            "interview_type": setup.get("interview_type", "mixed"),
            "experience_level": setup.get("experience_level", "2-5"),
        }, indent=2)

    @property
    def temperature(self) -> float:
        return 0.5
