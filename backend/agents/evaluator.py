import json
from typing import Any

from backend.agents.base import BaseAgent


class EvaluatorAgent(BaseAgent):
    name = "evaluator"
    prompt_name = "evaluator"

    def build_user_message(self, ctx: dict[str, Any]) -> str:
        return json.dumps({
            "turn": ctx.get("turn_number", 1),
            "question": ctx.get("current_question", ""),
            "answer": ctx.get("answer", ""),
            "interview_type": ctx.get("setup", {}).get("interview_type"),
            "target_role": ctx.get("setup", {}).get("target_role"),
        }, indent=2)

    @property
    def temperature(self) -> float:
        return 0.4
