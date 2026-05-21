# Example Transcript — Strong Candidate
**Role:** Senior Software Engineer · **Type:** Mixed

## Turn 1
**Interviewer:** What motivated you to pursue this role, and what would success look like in your first six months?

**Candidate:** I'm excited about scaling distributed systems at your scale. In month one I'd map critical services and on-call; by month six I'd own a reliability initiative with measurable SLO improvement.

**Evaluator JSON:**
```json
{
  "turn": 1,
  "scores": { "communication": 8, "technical_depth": 7, "structure": 8, "relevance": 9, "confidence": 8, "problem_solving": 7 },
  "strengths": ["Clear 30/180-day framing", "Confident delivery"],
  "weaknesses": ["Could cite a prior metric"],
  "improvement_tip": "Add one past win with a number.",
  "signal": "advance"
}
```

## Turn 2
**Interviewer:** Tell me about a project you're proud of — your specific contribution and measured impact.

**Candidate:** I led caching for our checkout API: designed Redis layer, cut p95 latency from 420ms to 180ms over 8 weeks, 4 engineers, $2M GMV at risk during peak.

**Evaluator:** `signal: advance` — scores 8–9 across dimensions.

## Turns 3–5
Structured STAR on conflict, solid system design trade-offs (read replicas, cache invalidation), thoughtful "decision I'd change" story.

## Turn 6 — Wrap up
**Evaluator:** `signal: wrap_up`

**Interviewer:** Thank you — we'll compile your feedback shortly.

---

## Coach Report Summary
- **Readiness:** Strong Candidate · **Score:** 84/100
- **Strengths:** Metrics-driven stories, system thinking, ownership
- **Gaps:** Minor — more failure-mode depth on design questions
- **Plan:** Maintain momentum; mock one staff-level design loop per week
