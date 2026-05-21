"""Pydantic models for InterviewPilot AI."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class InterviewType(str, Enum):
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    CASE = "case"
    MIXED = "mixed"


class ExperienceLevel(str, Enum):
    STUDENT = "student"
    ZERO_TO_TWO = "0-2"
    TWO_TO_FIVE = "2-5"
    FIVE_PLUS = "5+"


class EvalSignal(str, Enum):
    ADVANCE = "advance"
    PROBE = "probe"
    SIMPLIFY = "simplify"
    WRAP_UP = "wrap_up"


class SessionStartRequest(BaseModel):
    target_role: str = Field(..., min_length=2, max_length=200)
    background: str = Field(default="", max_length=8000)
    interview_type: InterviewType = InterviewType.MIXED
    experience_level: ExperienceLevel = ExperienceLevel.TWO_TO_FIVE


class TurnRequest(BaseModel):
    answer: str = Field(default="", max_length=10000)


class StrategistOutput(BaseModel):
    seniority: str = "mid"
    competencies_to_assess: list[str] = Field(default_factory=list)
    difficulty: str = "medium"
    opening_question_hint: str = ""
    candidate_flags: list[str] = Field(default_factory=list)
    interview_plan: str = ""


class EvaluatorOutput(BaseModel):
    turn: int = 0
    scores: dict[str, float] = Field(default_factory=dict)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    improvement_tip: str = ""
    signal: str = "advance"


SCORE_KEYS = [
    "communication",
    "technical_depth",
    "structure",
    "relevance",
    "confidence",
    "problem_solving",
]
