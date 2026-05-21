import json
from typing import Any

from backend.agents.base import BaseAgent


class InterviewerAgent(BaseAgent):
    name = "interviewer"
    prompt_name = "interviewer"

    def build_user_message(self, ctx: dict[str, Any]) -> str:
        history = [
            {"role": t.get("role"), "content": t.get("content")}
            for t in ctx.get("turns", ctx.get("transcript", []))
        ]
        return json.dumps({
            "strategy": ctx.get("strategy", {}),
            "turn_number": ctx.get("turn_number", 1),
            "conversation_history": history,
            "signal": ctx.get("current_signal", "advance"),
            "evaluator_summary": ctx.get("last_evaluation"),
            "setup": ctx.get("setup", {}),
        }, indent=2)

    async def run(self, ctx: dict[str, Any], *, json_mode: bool = True) -> str:
        from backend.utils.question_sanitize import normalize_interviewer_reply

        raw = await super().run(ctx, json_mode=False)  # type: ignore[return-value]
        return normalize_interviewer_reply(
            raw,
            ctx.get("strategy"),
            ctx.get("turn_number", 1),
        )

    @property
    def temperature(self) -> float:
        return 0.75
