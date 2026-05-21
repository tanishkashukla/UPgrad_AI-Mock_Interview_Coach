import json
from typing import Any

from backend.agents.base import BaseAgent


class CoachAgent(BaseAgent):
    name = "coach"
    prompt_name = "coach"

    def build_user_message(self, ctx: dict[str, Any]) -> str:
        return json.dumps({
            "setup": ctx.get("setup", {}),
            "strategy": ctx.get("strategy", {}),
            "evaluations": ctx.get("evaluations", []),
            "turns": ctx.get("turns", []),
            "aggregate_scores": ctx.get("aggregate_scores", {}),
        }, indent=2)

    async def run(self, ctx: dict[str, Any], *, json_mode: bool = True) -> str:
        return await super().run(ctx, json_mode=False)  # type: ignore[return-value]

    @property
    def temperature(self) -> float:
        return 0.6
