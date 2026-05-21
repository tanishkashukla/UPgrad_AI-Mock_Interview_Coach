"""OpenAI-compatible LLM client with mock mode."""
from __future__ import annotations

import json
import os
import re
from typing import Any

from openai import AsyncOpenAI

MOCK = os.getenv("MOCK_LLM", "false").lower() in ("1", "true", "yes")


class LLMClient:
    def __init__(self) -> None:
        key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.base_url = os.getenv("OPENAI_BASE_URL")
        self.mock = MOCK or not key
        self._client: AsyncOpenAI | None = None
        if not self.mock:
            kw: dict[str, Any] = {"api_key": key}
            if self.base_url:
                kw["base_url"] = self.base_url
            self._client = AsyncOpenAI(**kw, timeout=25.0)

    async def complete(
        self,
        system: str,
        user: str,
        *,
        json_mode: bool = False,
        temperature: float = 0.7,
        agent: str = "",
    ) -> str:
        if self.mock:
            return self._mock(agent, user, json_mode)
        assert self._client
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
        r = await self._client.chat.completions.create(**kwargs)
        return r.choices[0].message.content or ""

    def _mock(self, agent: str, user: str, json_mode: bool) -> str:
        role = (agent or "").lower()
        if role == "strategist":
            return json.dumps({
                "seniority": "mid",
                "competencies_to_assess": [
                    "communication", "problem solving", "technical depth", "ownership"
                ],
                "difficulty": "medium",
                "opening_question_hint": "Motivation and role fit",
                "candidate_flags": ["needs metrics on impact"],
                "interview_plan": "Open with motivation, deep-dive project, behavioral conflict, technical scenario, close.",
            })
        if role == "evaluator":
            turn = 1
            m = re.search(r'"turn":\s*(\d+)', user) or re.search(r'"turn_number":\s*(\d+)', user)
            if m:
                turn = int(m.group(1))
            sig = "advance" if turn < 5 else "wrap_up"
            if "don't know" in user.lower() or "[empty" in user.lower():
                sig = "simplify"
            elif "buzzword" in user.lower() or len(user) < 200:
                sig = "probe"
            return json.dumps({
                "turn": turn,
                "scores": {
                    "communication": 7.0, "technical_depth": 6.0, "structure": 6.5,
                    "relevance": 7.5, "confidence": 7.0, "problem_solving": 6.5,
                },
                "strengths": ["Clear tone", "Relevant example"],
                "weaknesses": ["Missing quantified outcome"],
                "improvement_tip": "End with a measurable result.",
                "signal": sig,
            })
        if role == "coach":
            return """# Interview Performance Report — InterviewPilot AI

## Executive Summary
Solid foundation with room to sharpen structure and technical depth.

## Readiness Level
**Interview Ready** — Score: **72/100**

## Skill Breakdown
| Dimension | Score |
|-----------|-------|
| Communication | 7.0 |
| Technical Depth | 6.0 |
| Structure | 6.5 |

## Top 3 Strengths
- Professional delivery
- Relevant examples
- Good engagement

## Top 3 Gaps
- Quantified impact
- Deeper trade-off reasoning
- Tighter STAR endings

## Better Sample Answers
**Q2:** I led a 4-person squad to cut p95 latency 38% in six weeks via caching and index tuning.

## 2-Week Practice Plan
### Week 1
- Write 5 STAR stories with metrics
- One mock technical daily

### Week 2
- Two system design whiteboards
- Record and review answers

## Learning Resources
- *Cracking the PM Interview* (if PM) / *Designing Data-Intensive Applications* (if SWE)

## Closing Note
You're closer than you think — consistent reps will get you there.
"""
        # Interviewer — plain text
        turn = 1
        m = re.search(r'"turn_number":\s*(\d+)', user)
        if m:
            turn = int(m.group(1))
        signal = "advance"
        sm = re.search(r'"signal":\s*"(\w+)"', user)
        if sm:
            signal = sm.group(1)
        qs = [
            "Thanks for joining today. To start — what draws you to this role, and what would success look like in your first six months?",
            "Tell me about a project you're proud of. What was **your** specific contribution and how did you measure impact?",
            "When you and a teammate disagreed on approach, how did you resolve it? Walk me through the situation and outcome.",
            "How would you design an API that needs to handle 10x read traffic with minimal downtime? Talk me through trade-offs.",
            "Describe a decision you would make differently today. What did you learn?",
            "Before we wrap — what's one skill you're actively improving, and how are you practicing it?",
        ]
        if signal == "wrap_up" or turn >= 5:
            return "That's a great place to end. Thank you for your thoughtful answers today — we'll compile your feedback report shortly."
        
        prev_idx = max(0, turn - 2)
        if signal == "probe":
            probes = [
                "That's interesting. Can you expand on how this role specifically aligns with your long-term career goals?",
                "Interesting — can you go deeper on the **specific metrics** and what **you personally** built versus the team?",
                "I see. What specific compromise did you reach, and how did it affect the team's project outcome?",
                "How would you monitor and measure the success of this technical solution once deployed?",
                "How do you plan to apply this new skill to a real-world project in the near future?"
            ]
            return probes[min(prev_idx, len(probes) - 1)]
            
        if signal == "simplify":
            simplifies = [
                "No worries! To keep it simple: what is one thing you enjoyed doing in your previous work or projects?",
                "No worries — let's try a simpler angle: describe a recent task you completed step by step, even if it was small.",
                "No problem. Let's make it simpler: tell me about a time you worked with someone to get something done.",
                "That's fine! Just describe the first tool or approach you would use to start tackling the issue.",
                "No worries. What is a tool or topic you've read about recently that you found interesting?"
            ]
            return simplifies[min(prev_idx, len(simplifies) - 1)]
            
        idx = min(turn - 1, len(qs) - 1)
        return qs[idx]
