# Example Transcript — Edge Case Candidate
**Role:** Data Analyst · **Type:** Mixed

## Turn 1 — Normal opening
**Evaluator:** `signal: advance`

## Turn 2 — "I don't know"
**Interviewer:** How would you validate an A/B test that looks positive but has uneven segment sizes?

**Candidate:** I don't know — we usually let the data team handle that.

**Evaluator:**
```json
{
  "turn": 2,
  "scores": { "communication": 6, "technical_depth": 3, "structure": 4, "relevance": 5, "confidence": 4, "problem_solving": 3 },
  "strengths": ["Honest about gap"],
  "weaknesses": ["No attempt at framework"],
  "improvement_tip": "Offer a simple approach: check sample ratio mismatch, SRM test, segment breakdown.",
  "signal": "simplify"
}
```

**Interviewer:** No worries — even a simple approach works: how would you check if traffic split was fair before trusting uplift?

## Turn 3 — Off-topic
**Candidate:** Speaking of traffic, I love traveling to Japan...

**Evaluator:** `signal: probe` — relevance 3.

**Interviewer:** Let's refocus on the experiment — what metrics would you watch besides conversion rate?

## Turn 4 — Partial correctness
**Candidate:** I'd check p-value and maybe confidence intervals. Sample size matters too but I'm fuzzy on power.

**Evaluator:** `signal: probe` — acknowledges partial stats knowledge; technical_depth 5.

**Interviewer:** Good start on inference — how would you explain statistical power to a PM in one sentence?

## Turns 5–6 — Recovery then wrap_up
Candidate gives adequate SQL example with one metric; final `signal: wrap_up`.

## Coach Report Summary
- **Readiness:** Developing · **Score:** 58/100
- **Noted:** Handled IDK and off-topic gracefully in interview flow
- **Plan:** A/B testing course module + 3 written post-mortems of past experiments
