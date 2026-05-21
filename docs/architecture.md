# InterviewPilot AI — Architecture

## Orchestrator (`backend/services/orchestrator.py`)

Owns session lifecycle and agent coordination:

1. `start_session` → Strategist → Interviewer (turn 1)
2. `process_turn` → Evaluator → (optional Coach if complete) → Interviewer
3. `generate_report` → Coach (idempotent)

## Session State

```python
{
  "session_id": str,
  "strategy": dict,
  "turns": list,
  "evaluations": list,
  "current_signal": str,
  "current_turn": int,
  "interview_complete": bool,
  "final_report": str | None,
  "aggregate_scores": dict,
  "overall_score": float,
  "readiness_label": str,
}
```

## Prompt Files

| File | Agent | Output |
|------|-------|--------|
| `prompts/strategist.md` | Strategist | JSON |
| `prompts/interviewer.md` | Interviewer | Plain text |
| `prompts/evaluator.md` | Evaluator | JSON + signal |
| `prompts/coach.md` | Coach | Markdown |
