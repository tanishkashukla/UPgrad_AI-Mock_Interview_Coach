"""Evaluator Agent — scores each answer in real time."""
from __future__ import annotations

import json
from typing import Any

from agents.base_agent import BaseAgent


class EvaluatorAgent(BaseAgent):
    name = "evaluator"
    prompt_file = "evaluator"

    def build_user_message(self, context: dict[str, Any]) -> str:
        return json.dumps({
            "question_asked": context.get("current_question", ""),
            "candidate_answer": context.get("answer", ""),
            "turn_number": context.get("turn_number", 0),
            "interview_type": context.get("setup", {}).get("interview_type", "mixed"),
            "target_role": context.get("setup", {}).get("target_role", ""),
            "prior_evaluations_summary": context.get("prior_eval_summary"),
        }, indent=2)

    @property
    def temperature(self) -> float:
        return 0.4
