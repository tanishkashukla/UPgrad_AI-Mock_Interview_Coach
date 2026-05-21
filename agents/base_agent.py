"""Base agent class for InterviewIQ multi-agent system."""
from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.llm_client import LLMClient
from services.prompt_loader import load_prompt
from utils.json_parser import extract_json


class BaseAgent(ABC):
    name: str = "base"
    prompt_file: str = ""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or LLMClient()
        self._system_prompt: str | None = None

    @property
    def system_prompt(self) -> str:
        if self._system_prompt is None:
            self._system_prompt = load_prompt(self.prompt_file)
        return self._system_prompt

    @abstractmethod
    def build_user_message(self, context: dict[str, Any]) -> str:
        ...

    async def run(self, context: dict[str, Any], *, json_mode: bool = True) -> Any:
        user_msg = self.build_user_message(context)
        raw = await self.llm.complete(
            self.system_prompt,
            user_msg,
            json_mode=json_mode,
            temperature=self.temperature,
        )
        if json_mode:
            return extract_json(raw)
        return raw

    @property
    def temperature(self) -> float:
        return 0.7
