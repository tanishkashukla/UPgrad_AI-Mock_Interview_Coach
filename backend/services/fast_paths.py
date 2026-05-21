"""Instant responses for mock/demo mode — no LLM latency."""
from __future__ import annotations

import re
from typing import Any

FIRST_QUESTIONS = [
    "Thanks for joining today. To start — what draws you to this role, and what would success look like in your first six months?",
    "Tell me about a project you're proud of. What was your specific contribution, and how did you measure impact?",
    "Describe a time you disagreed with a teammate. How did you handle it, and what was the outcome?",
    "How would you approach a technical problem you've never seen before? Walk me through your thinking.",
    "Before we wrap up — what's one skill you're actively improving, and how are you practicing it?",
]


def mock_strategy(setup: dict[str, Any]) -> dict[str, Any]:
    role = setup.get("target_role", "the role")
    return {
        "seniority": "mid",
        "competencies_to_assess": [
            "communication",
            "problem solving",
            "technical depth",
            "ownership",
        ],
        "difficulty": "medium",
        "opening_question_hint": f"Motivation and fit for {role}",
        "candidate_flags": ["probe for measurable impact"],
        "interview_plan": f"Five-question mixed interview for {role}: motivation, project, behavioral, technical thinking, close.",
    }


def first_question_from_strategy(strategy: dict[str, Any], setup: dict[str, Any]) -> str:
    """Build Q1 from strategist output — avoids a second LLM call on session start."""
    role = setup.get("target_role", "this role")
    hint = strategy.get("opening_question_hint") or "your motivation and fit"
    hint = hint.strip().rstrip(".")
    return (
        f"Thanks for joining today. For the {role} position — focusing on {hint.lower()} — "
        "what draws you to this opportunity, and what would success look like in your first six months?"
    )


def mock_evaluation(turn: int, answer: str) -> dict[str, Any]:
    sig = "advance"
    if turn >= 5:
        sig = "wrap_up"
    elif "don't know" in answer.lower() or len(answer.strip()) < 15:
        sig = "simplify"
    elif len(answer) < 120:
        sig = "probe"
    return {
        "turn": turn,
        "scores": {
            "communication": 7.0,
            "technical_depth": 6.5,
            "structure": 6.5,
            "relevance": 7.5,
            "confidence": 7.0,
            "problem_solving": 6.5,
        },
        "strengths": ["Clear communication", "Relevant example"],
        "weaknesses": ["Add specific metrics to strengthen impact"],
        "improvement_tip": "Close with a quantified result when possible.",
        "signal": sig,
    }


def mock_interviewer_question(turn: int, signal: str) -> str:
    if signal == "wrap_up" or turn >= 5:
        return (
            "That's a great place to end. Thank you for your thoughtful answers — "
            "we'll compile your feedback report now."
        )
    
    prev_idx = max(0, turn - 2)
    
    if signal == "probe":
        probes = [
            "That's interesting. Can you expand on how this role specifically aligns with your long-term career goals?",
            "Can you go deeper on the specific metrics and what you personally owned versus the broader team?",
            "I see. What specific compromise did you reach, and how did it affect the team's project outcome?",
            "How would you monitor and measure the success of this technical solution once deployed?",
            "How do you plan to apply this new skill to a real-world project in the near future?"
        ]
        return probes[min(prev_idx, len(probes) - 1)]
        
    if signal == "simplify":
        simplifies = [
            "No worries! To keep it simple: what is one thing you enjoyed doing in your previous work or projects?",
            "No worries — try a simpler angle: walk me through a recent task you completed step by step.",
            "No problem. Let's make it simpler: tell me about a time you worked with someone to get something done.",
            "That's fine! Just describe the first tool or approach you would use to start tackling the issue.",
            "No worries. What is a tool or topic you've read about recently that you found interesting?"
        ]
        return simplifies[min(prev_idx, len(simplifies) - 1)]
        
    return FIRST_QUESTIONS[min(turn - 1, len(FIRST_QUESTIONS) - 1)]
