"""Multi-agent orchestration pipeline for InterviewIQ AI."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.agent_manager import AgentManager
from services.state_manager import StateManager


SCORE_KEYS = [
    "communication", "technical_depth", "clarity", "structure",
    "confidence", "leadership", "relevance", "critical_thinking", "problem_solving",
]


class InterviewOrchestrator:
    def __init__(self) -> None:
        self.agents = AgentManager()
        self.state = StateManager()

    async def start_session(self, setup: dict[str, Any]) -> dict[str, Any]:
        session_id = self.state.new_session_id()
        state: dict[str, Any] = {
            "session_id": session_id,
            "setup": setup,
            "strategy": None,
            "status": "active",
            "current_turn": 0,
            "min_turns": 5,
            "max_turns": 7,
            "transcript": [],
            "evaluations": [],
            "latest_evaluator_feedback": None,
            "current_question": None,
            "final_report_markdown": None,
            "aggregate_scores": {},
            "overall_score": 0.0,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        # Step 1: Strategist
        strategy = await self.agents.strategist.run({"setup": setup})
        state["strategy"] = strategy

        # Step 2: Interviewer — first question
        state["current_turn"] = 1
        interviewer_out = await self.agents.interviewer.run({
            "setup": setup,
            "strategy": strategy,
            "turn_number": 1,
            "transcript": [],
            "evaluator_feedback": None,
        })
        question = interviewer_out.get("message", "Tell me about yourself and your interest in this role.")
        state["current_question"] = question
        state["transcript"].append({
            "role": "interviewer",
            "content": question,
            "turn_number": 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        await self.state.save(state)
        return {
            "session_id": session_id,
            "strategy": strategy,
            "first_question": question,
            "turn_number": 1,
            "agent_activity": self.agents.activity_for("interview_start"),
        }

    def _aggregate_scores(self, evaluations: list[dict[str, Any]]) -> dict[str, float]:
        if not evaluations:
            return {k: 0.0 for k in SCORE_KEYS}
        totals = {k: 0.0 for k in SCORE_KEYS}
        count = 0
        for ev in evaluations:
            scores = ev.get("scores", {})
            if not scores:
                continue
            count += 1
            for k in SCORE_KEYS:
                totals[k] += float(scores.get(k, 0))
        if count == 0:
            return totals
        return {k: round(totals[k] / count, 2) for k in SCORE_KEYS}

    def _overall_score(self, evaluations: list[dict[str, Any]]) -> float:
        if not evaluations:
            return 0.0
        vals = [float(e.get("overall_turn_score", 0)) for e in evaluations]
        return round(sum(vals) / len(vals) * 10, 1) if vals else 0.0  # scale to 0-100

    async def submit_answer(self, session_id: str, answer: str) -> dict[str, Any]:
        state = await self.state.load(session_id)
        if not state:
            raise ValueError("Session not found")
        if state.get("status") == "completed":
            raise ValueError("Session already completed")

        answer = (answer or "").strip()
        turn = state["current_turn"]

        # Record candidate answer
        state["transcript"].append({
            "role": "candidate",
            "content": answer or "[empty answer]",
            "turn_number": turn,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        # Step 3: Evaluator
        evaluation = await self.agents.evaluator.run({
            "setup": state["setup"],
            "current_question": state.get("current_question", ""),
            "answer": answer,
            "turn_number": turn,
            "prior_eval_summary": state["evaluations"][-2:] if state["evaluations"] else None,
        })
        state["evaluations"].append(evaluation)
        state["latest_evaluator_feedback"] = evaluation
        state["aggregate_scores"] = self._aggregate_scores(state["evaluations"])
        state["overall_score"] = self._overall_score(state["evaluations"])

        # Check completion
        interviewer_out = await self.agents.interviewer.run({
            "setup": state["setup"],
            "strategy": state["strategy"],
            "turn_number": turn + 1,
            "transcript": state["transcript"],
            "evaluator_feedback": evaluation.get("interviewer_hints", evaluation),
        })

        is_wrap = interviewer_out.get("is_wrap_up", False)
        at_max = turn >= state.get("max_turns", 7)
        at_min = turn >= state.get("min_turns", 5)

        if is_wrap and at_min or at_max:
            # Step 4: Career Coach final report
            report = await self.agents.coach.run({
                "setup": state["setup"],
                "strategy": state["strategy"],
                "evaluations": state["evaluations"],
                "transcript": state["transcript"],
                "turn_number": turn,
                "aggregate_scores": state["aggregate_scores"],
            })
            state["final_report_markdown"] = report
            state["status"] = "completed"
            await self.state.save(state)
            return {
                "session_id": session_id,
                "evaluation": evaluation,
                "next_question": None,
                "turn_number": turn,
                "is_complete": True,
                "agent_activity": self.agents.activity_for("report"),
                "aggregate_scores": state["aggregate_scores"],
            }

        # Continue interview
        next_q = interviewer_out.get("message", "Let's continue — can you elaborate on your last point?")
        state["current_turn"] = turn + 1
        state["current_question"] = next_q
        state["transcript"].append({
            "role": "interviewer",
            "content": next_q,
            "turn_number": turn + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        await self.state.save(state)

        return {
            "session_id": session_id,
            "evaluation": evaluation,
            "next_question": next_q,
            "turn_number": turn + 1,
            "is_complete": False,
            "agent_activity": self.agents.activity_for("adapt"),
            "aggregate_scores": state["aggregate_scores"],
        }

    async def retry_last_answer(self, session_id: str, answer: str) -> dict[str, Any]:
        """Allow candidate to retry their last answer."""
        state = await self.state.load(session_id)
        if not state:
            raise ValueError("Session not found")
        # Pop last candidate message and re-evaluate
        while state["transcript"] and state["transcript"][-1].get("role") == "candidate":
            state["transcript"].pop()
        if state["evaluations"]:
            state["evaluations"].pop()
        await self.state.save(state)
        return await self.submit_answer(session_id, answer)

    async def get_session(self, session_id: str) -> dict[str, Any] | None:
        return await self.state.load(session_id)

    async def list_history(self) -> list[dict[str, Any]]:
        return await self.state.list_sessions()
