"""Shared Pydantic schemas for InterviewIQ AI."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class InterviewType(str, Enum):
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    MIXED = "mixed"
    SYSTEM_DESIGN = "system_design"
    LEADERSHIP = "leadership"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    ADAPTIVE = "adaptive"


class ExperienceLevel(str, Enum):
    INTERN = "intern"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"


class SessionSetup(BaseModel):
    target_role: str = Field(..., min_length=2, max_length=200)
    resume_snippet: str = Field(default="", max_length=8000)
    interview_type: InterviewType = InterviewType.MIXED
    difficulty: Difficulty = Difficulty.ADAPTIVE
    experience_level: ExperienceLevel = ExperienceLevel.MID


class TurnMessage(BaseModel):
    role: str  # interviewer | candidate
    content: str
    turn_number: int = 0
    timestamp: datetime | None = None


class EvaluatorOutput(BaseModel):
    scores: dict[str, float] = Field(default_factory=dict)
    overall_turn_score: float = 0.0
    star_analysis: dict[str, Any] = Field(default_factory=dict)
    answer_quality: str = "fair"
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    missed_opportunities: list[str] = Field(default_factory=list)
    better_sample_answer: str = ""
    improvement_tips: list[str] = Field(default_factory=list)
    interviewer_hints: dict[str, Any] = Field(default_factory=dict)


class StrategistOutput(BaseModel):
    skill_level: str = "mid"
    estimated_readiness: int = 50
    interview_roadmap: list[dict[str, Any]] = Field(default_factory=list)
    behavioral_ratio: int = 50
    technical_ratio: int = 50
    difficulty_plan: dict[str, Any] = Field(default_factory=dict)
    probing_strategy: dict[str, Any] = Field(default_factory=dict)
    key_competencies: list[str] = Field(default_factory=list)
    interviewer_guidance: str = ""


class InterviewerOutput(BaseModel):
    message: str
    internal_notes: str = ""
    turn_theme: str = ""
    difficulty_level: str = "medium"
    is_wrap_up: bool = False
    probing_type: str = "opening"


class SessionState(BaseModel):
    session_id: str
    setup: SessionSetup
    strategy: StrategistOutput | dict[str, Any] | None = None
    status: str = "setup"  # setup | active | completed
    current_turn: int = 0
    min_turns: int = 5
    max_turns: int = 7
    transcript: list[TurnMessage] = Field(default_factory=list)
    evaluations: list[EvaluatorOutput | dict[str, Any]] = Field(default_factory=list)
    latest_evaluator_feedback: dict[str, Any] | None = None
    current_question: str | None = None
    final_report_markdown: str | None = None
    aggregate_scores: dict[str, float] = Field(default_factory=dict)
    overall_score: float = 0.0
    created_at: datetime | None = None
    updated_at: datetime | None = None


class StartSessionResponse(BaseModel):
    session_id: str
    strategy: dict[str, Any]
    first_question: str
    turn_number: int
    agent_activity: list[str]


class AnswerRequest(BaseModel):
    session_id: str
    answer: str = Field(default="", max_length=10000)


class AnswerResponse(BaseModel):
    session_id: str
    evaluation: dict[str, Any]
    next_question: str | None = None
    turn_number: int
    is_complete: bool = False
    agent_activity: list[str]
    aggregate_scores: dict[str, float] = Field(default_factory=dict)


class SessionSummary(BaseModel):
    session_id: str
    target_role: str
    interview_type: str
    status: str
    overall_score: float
    turn_count: int
    created_at: str | None = None
