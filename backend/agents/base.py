from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from backend.services.prompt_loader import load_prompt
from backend.utils.json_parser import extract_json
from backend.utils.llm_client import LLMClient


class BaseAgent(ABC):
    name = "base"
    prompt_name = ""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or LLMClient()
        self._prompt: str | None = None

    @property
    def system_prompt(self) -> str:
        if self._prompt is None:
            self._prompt = load_prompt(self.prompt_name)
        return self._prompt

    @abstractmethod
    def build_user_message(self, ctx: dict[str, Any]) -> str: ...

    @property
    def temperature(self) -> float:
        return 0.7

    async def run(self, ctx: dict[str, Any], *, json_mode: bool = True) -> Any:
        raw = await self.llm.complete(
            self.system_prompt,
            self.build_user_message(ctx),
            json_mode=json_mode,
            temperature=self.temperature,
            agent=self.name,
        )
        if json_mode:
            return extract_json(raw)
        return raw.strip()
