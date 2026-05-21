"""Central multi-agent orchestrator for InterviewPilot AI."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from backend.agents.coach import CoachAgent
from backend.agents.evaluator import EvaluatorAgent
from backend.agents.interviewer import InterviewerAgent
from backend.agents.strategist import StrategistAgent
from backend.db.database import SessionDatabase
from backend.state.models import SCORE_KEYS
from backend.services.fast_paths import (
    first_question_from_strategy,
    mock_evaluation,
    mock_interviewer_question,
    mock_strategy,
)
from backend.utils.llm_client import LLMClient
from backend.utils.question_sanitize import normalize_interviewer_reply

# Fixed 5-question interview (assignment: 5–7 turns; we use 5 for consistent UX)
MIN_TURNS = 5
MAX_TURNS = 5
TOTAL_QUESTIONS = 5


def _use_fast_path(llm: LLMClient) -> bool:
    """Instant local responses for demo (no API wait)."""
    mock_env = os.getenv("MOCK_LLM", "true").lower() in ("1", "true", "yes")
    return llm.mock or mock_env


class Orchestrator:
    def __init__(self) -> None:
        llm = LLMClient()
        self.db = SessionDatabase()
        self.strategist = StrategistAgent(llm)
        self.interviewer = InterviewerAgent(llm)
        self.evaluator = EvaluatorAgent(llm)
        self.coach = CoachAgent(llm)

    def _empty_state(self, session_id: str, setup: dict[str, Any]) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "setup": setup,
            "strategy": None,
            "turns": [],
            "evaluations": [],
            "current_signal": "advance",
            "current_turn": 0,
            "current_question": None,
            "interview_complete": False,
            "final_report": None,
            "aggregate_scores": {},
            "overall_score": 0.0,
            "readiness_label": "",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def _avg_scores(self, evals: list[dict[str, Any]]) -> dict[str, float]:
        if not evals:
            return {k: 0.0 for k in SCORE_KEYS}
        totals = {k: 0.0 for k in SCORE_KEYS}
        n = 0
        for ev in evals:
            sc = ev.get("scores", {})
            if not sc:
                continue
            n += 1
            for k in SCORE_KEYS:
                totals[k] += float(sc.get(k, 0))
        if n == 0:
            return totals
        return {k: round(totals[k] / n, 2) for k in SCORE_KEYS}

    def _overall(self, evals: list[dict[str, Any]]) -> float:
        if not evals:
            return 0.0
        all_sc = []
        for ev in evals:
            all_sc.extend(float(v) for v in ev.get("scores", {}).values())
        return round(sum(all_sc) / len(all_sc) * 10, 1) if all_sc else 0.0

    def _readiness(self, score: float) -> str:
        if score >= 80:
            return "Strong Candidate"
        if score >= 65:
            return "Interview Ready"
        if score >= 45:
            return "Developing"
        return "Not Ready"

    async def start_session(self, setup: dict[str, Any]) -> dict[str, Any]:
        sid = self.db.new_id()
        state = self._empty_state(sid, setup)
        llm = self.strategist.llm

        # Mock/demo: instant — no network calls
        if _use_fast_path(llm):
            state["strategy"] = mock_strategy(setup)
            question = first_question_from_strategy(state["strategy"], setup)
        else:
            state["strategy"] = await self.strategist.run({"setup": setup})
            # One LLM call only; Q1 from strategy (faster than second interviewer call)
            question = first_question_from_strategy(state["strategy"], setup)
            question = normalize_interviewer_reply(question, state["strategy"], turn=1)

        state["current_turn"] = 1
        state["current_signal"] = "advance"
        state["current_question"] = question
        state["turns"].append({
            "role": "interviewer",
            "content": question,
            "turn": 1,
            "ts": datetime.now(timezone.utc).isoformat(),
        })

        await self.db.save(state)
        return {
            "session_id": sid,
            "first_question": question,
            "strategy": state["strategy"],
            "turn": 1,
            "max_turns": TOTAL_QUESTIONS,
            "total_questions": TOTAL_QUESTIONS,
            "agents_active": ["Profile Strategist", "Interviewer"],
        }

    async def process_turn(self, session_id: str, answer: str) -> dict[str, Any]:
        state = await self.db.load(session_id)
        if not state:
            raise ValueError("Session not found")
        if state.get("interview_complete"):
            raise ValueError("Interview already complete")

        turn = state["current_turn"]
        answer = (answer or "").strip()

        state["turns"].append({
            "role": "candidate",
            "content": answer or "[empty answer]",
            "turn": turn,
            "ts": datetime.now(timezone.utc).isoformat(),
        })

        prev_signal = state.get("current_signal", "advance")

        if _use_fast_path(self.evaluator.llm):
            evaluation = mock_evaluation(turn, answer)
        else:
            evaluation = await self.evaluator.run({
                "setup": state["setup"],
                "current_question": state["current_question"],
                "answer": answer,
                "turn_number": turn,
            })
            evaluation["turn"] = turn

        # If the previous question was already a follow-up (probe or simplify),
        # force the new signal to "advance" to ensure the interview progresses.
        if prev_signal in ("probe", "simplify"):
            evaluation["signal"] = "advance"

        state["evaluations"].append(evaluation)
        signal = evaluation.get("signal", "advance")
        state["current_signal"] = signal
        state["aggregate_scores"] = self._avg_scores(state["evaluations"])
        state["overall_score"] = self._overall(state["evaluations"])
        state["readiness_label"] = self._readiness(state["overall_score"])

        eval_count = len(state["evaluations"])
        # End after 5 answers (5 questions). Also honor wrap_up once minimum met.
        should_end = eval_count >= MAX_TURNS or (
            eval_count >= MIN_TURNS and signal == "wrap_up"
        )

        if should_end:
            report = await self.coach.run({
                "setup": state["setup"],
                "strategy": state["strategy"],
                "evaluations": state["evaluations"],
                "turns": state["turns"],
                "aggregate_scores": state["aggregate_scores"],
            })
            state["final_report"] = report
            state["interview_complete"] = True
            await self.db.save(state)
            return {
                "session_id": session_id,
                "evaluation": evaluation,
                "live_scores": state["aggregate_scores"],
                "signal": signal,
                "turn": turn,
                "interview_complete": True,
                "next_question": None,
                "agents_active": ["Real-Time Evaluator", "AI Career Coach"],
                "overall_score": state["overall_score"],
                "readiness_label": state["readiness_label"],
            }

        next_turn = turn + 1
        if _use_fast_path(self.interviewer.llm):
            next_q = mock_interviewer_question(next_turn, signal)
        else:
            raw_next = await self.interviewer.run({
                "setup": state["setup"],
                "strategy": state["strategy"],
                "turn_number": next_turn,
                "turns": state["turns"],
                "current_signal": signal,
                "last_evaluation": {
                    "strengths": evaluation.get("strengths"),
                    "weaknesses": evaluation.get("weaknesses"),
                    "improvement_tip": evaluation.get("improvement_tip"),
                    "signal": signal,
                },
            })
            next_q = normalize_interviewer_reply(raw_next, state["strategy"], turn=next_turn)

        state["current_turn"] = turn + 1
        state["current_question"] = next_q
        state["turns"].append({
            "role": "interviewer",
            "content": next_q,
            "turn": turn + 1,
            "ts": datetime.now(timezone.utc).isoformat(),
        })
        await self.db.save(state)

        return {
            "session_id": session_id,
            "evaluation": evaluation,
            "live_scores": state["aggregate_scores"],
            "signal": signal,
            "turn": turn,
            "next_turn": turn + 1,
            "next_question": next_q,
            "interview_complete": False,
            "total_questions": TOTAL_QUESTIONS,
            "agents_active": ["Real-Time Evaluator", "Interviewer"],
            "overall_score": state["overall_score"],
            "readiness_label": state["readiness_label"],
        }

    async def generate_report(self, session_id: str) -> dict[str, Any]:
        state = await self.db.load(session_id)
        if not state:
            raise ValueError("Session not found")
        if not state.get("final_report"):
            report = await self.coach.run({
                "setup": state["setup"],
                "strategy": state["strategy"],
                "evaluations": state["evaluations"],
                "turns": state["turns"],
                "aggregate_scores": state["aggregate_scores"],
            })
            state["final_report"] = report
            state["interview_complete"] = True
            await self.db.save(state)
        return {
            "session_id": session_id,
            "report_markdown": state["final_report"],
            "overall_score": state.get("overall_score", 0),
            "readiness_label": state.get("readiness_label", ""),
            "aggregate_scores": state.get("aggregate_scores", {}),
        }

    async def get_history(self, session_id: str) -> dict[str, Any]:
        state = await self.db.load(session_id)
        if not state:
            raise ValueError("Session not found")
        return state

    async def list_sessions(self) -> list[dict[str, Any]]:
        return await self.db.list_all()

    async def delete_session(self, session_id: str) -> bool:
        return await self.db.delete(session_id)
