"""Central registry for all InterviewIQ agents."""
from __future__ import annotations

from agents.coach import CoachAgent
from agents.evaluator import EvaluatorAgent
from agents.interviewer import InterviewerAgent
from agents.strategist import StrategistAgent
from services.llm_client import LLMClient


class AgentManager:
    def __init__(self, llm: LLMClient | None = None) -> None:
        llm = llm or LLMClient()
        self.strategist = StrategistAgent(llm)
        self.interviewer = InterviewerAgent(llm)
        self.evaluator = EvaluatorAgent(llm)
        self.coach = CoachAgent(llm)

    def activity_for(self, step: str) -> list[str]:
        mapping = {
            "strategy": ["Strategist", "Planning roadmap"],
            "interview_start": ["Strategist", "Interviewer"],
            "evaluate": ["Evaluator", "Analyzing response"],
            "adapt": ["Evaluator", "Interviewer", "Adapting next question"],
            "report": ["Career Coach", "Generating final report"],
        }
        return mapping.get(step, ["Orchestrator"])
