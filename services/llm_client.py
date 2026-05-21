"""OpenAI client with mock fallback for demo without API key."""
from __future__ import annotations

import json
import os
from typing import Any

from openai import AsyncOpenAI

MOCK_MODE = os.getenv("MOCK_LLM", "false").lower() in ("1", "true", "yes")


class LLMClient:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.mock = MOCK_MODE or not api_key
        self._client: AsyncOpenAI | None = None
        if not self.mock:
            self._client = AsyncOpenAI(api_key=api_key)

    async def complete(
        self,
        system: str,
        user: str,
        *,
        json_mode: bool = True,
        temperature: float = 0.7,
    ) -> str:
        if self.mock:
            return self._mock_response(system, user, json_mode)

        assert self._client is not None
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        resp = await self._client.chat.completions.create(**kwargs)
        return resp.choices[0].message.content or ""

    def _mock_response(self, system: str, user: str, json_mode: bool) -> str:
        """Deterministic mock outputs for development without API key."""
        if "STRATEGIST" in system.upper() or "strategist" in system.lower():
            return json.dumps({
                "skill_level": "mid",
                "estimated_readiness": 62,
                "interview_roadmap": [
                    {"turn": i, "theme": t, "focus": "behavioral" if i % 2 else "technical", "objective": f"Assess {t}"}
                    for i, t in enumerate(
                        ["Introduction & motivation", "Past project deep-dive", "Conflict resolution",
                         "Technical problem-solving", "System thinking", "Leadership scenario", "Closing reflection"],
                        1,
                    )
                ],
                "behavioral_ratio": 55,
                "technical_ratio": 45,
                "difficulty_plan": {
                    "starting": "medium",
                    "escalation_triggers": ["strong technical answer", "detailed STAR story"],
                    "deescalation_triggers": ["I don't know", "very short answer"],
                },
                "probing_strategy": {
                    "weak_areas": ["metrics for impact", "trade-off reasoning"],
                    "resume_topics": ["recent project", "team collaboration"],
                    "follow_up_depth": "medium",
                },
                "key_competencies": ["communication", "problem solving", "ownership"],
                "interviewer_guidance": "Start warm, probe resume project by turn 2, escalate if strong.",
            })
        if "INTERVIEWER" in system.upper():
            turn = 1
            if '"turn_number"' in user:
                import re
                m = re.search(r'"turn_number":\s*(\d+)', user)
                if m:
                    turn = int(m.group(1))
            questions = [
                "Welcome! To start, tell me about yourself and what specifically draws you to this role.",
                "Walk me through a challenging project from your background — what was your role and the outcome?",
                "Describe a time you disagreed with a teammate. How did you handle it?",
                "How would you approach designing a scalable API for high read traffic? Talk me through your thinking.",
                "Tell me about a technical decision you later regretted. What would you do differently?",
                "How do you mentor or unblock junior engineers on your team?",
                "Before we wrap up — what questions do you have for us, and what's your biggest growth area?",
            ]
            idx = min(turn - 1, len(questions) - 1)
            wrap = turn >= 5
            return json.dumps({
                "message": questions[idx],
                "internal_notes": f"Mock question for turn {turn}",
                "turn_theme": f"Turn {turn}",
                "difficulty_level": "medium",
                "is_wrap_up": wrap and turn >= 7,
                "probing_type": "opening" if turn == 1 else "follow_up",
            })
        if "EVALUATOR" in system.upper():
            return json.dumps({
                "scores": {
                    "communication": 7.0, "technical_depth": 6.5, "clarity": 7.0,
                    "structure": 6.0, "confidence": 7.5, "leadership": 6.0,
                    "relevance": 7.0, "critical_thinking": 6.5, "problem_solving": 6.5,
                },
                "overall_turn_score": 6.8,
                "star_analysis": {"situation": True, "task": True, "action": True, "result": False, "star_score": 7.0},
                "answer_quality": "good",
                "strengths": ["Clear narrative flow", "Relevant example chosen"],
                "weaknesses": ["Missing quantified results", "Could be more concise"],
                "missed_opportunities": ["Did not mention team size or timeline"],
                "better_sample_answer": "I led a 4-person team to reduce API latency by 40% over 6 weeks by introducing caching and query optimization.",
                "improvement_tips": ["End with measurable impact", "Use STAR structure explicitly"],
                "interviewer_hints": {
                    "should_probe_deeper": True,
                    "should_simplify": False,
                    "suggested_follow_up_angle": "Ask for specific metrics and your personal contribution",
                },
            })
        # Coach returns markdown
        return """# Interview Performance Report — InterviewIQ AI

## Executive Summary
You demonstrated solid communication and relevant examples. Technical depth can improve with more structured problem-solving narratives.

## Interview Readiness Level
**Level:** Nearly Ready
**Score:** 68/100

## Performance Snapshot
| Dimension | Score | Notes |
|-----------|-------|-------|
| Communication | 7.0 | Clear and professional |
| Technical Depth | 6.5 | Good foundation, needs metrics |
| Structure | 6.0 | Practice STAR endings |

## Key Strengths
- Professional tone and engagement
- Relevant real-world examples

## Areas for Improvement
- Quantify impact with numbers
- Deeper technical trade-off discussion

## Personalized Improvement Roadmap
### Week 1
Practice 5 STAR stories with metrics.

### Week 2
Mock system design 2x per week.

## Final Coaching Note
You're closer than you think — consistent practice will get you interview-ready. Keep going!
"""
