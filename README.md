# InterviewPilot AI

**Practice smarter. Interview better.**

Production-grade multi-agent mock interview platform — four genuinely distinct AI agents, signal-driven orchestration, and a premium Next.js frontend.

## Quick Start

### Local (recommended)

```powershell
cd "d:\UpGrad - AI Mock Interview Coach"
.\start.ps1
```

Or manually:

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r backend\requirements.txt
$env:PYTHONPATH = (Get-Location).Path
$env:MOCK_LLM = "true"
.\.venv\Scripts\uvicorn.exe backend.main:app --reload --port 8000

cd frontend
npm install
$env:NEXT_PUBLIC_API_URL = "http://127.0.0.1:8000"
npm run dev
```

Open **http://localhost:3000**

### Docker

```bash
docker compose up --build
```

Set `MOCK_LLM=false` and `OPENAI_API_KEY` in `.env` for live LLM calls.

## Architecture

```
User → Next.js → FastAPI Orchestrator
                    ├── Profile Strategist (JSON strategy)
                    ├── Interviewer (plain text, uses signal)
                    ├── Real-Time Evaluator (JSON + signal)
                    └── AI Career Coach (markdown report)
                              ↓
                         SQLite sessions
```

See [docs/architecture.md](docs/architecture.md).

## Agent Responsibilities

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Profile Strategist** | Pre-interview planning | Role, background, type, level | JSON strategy |
| **Interviewer** | Live adaptive dialogue | History + evaluator signal | Plain text question |
| **Real-Time Evaluator** | Per-turn scoring | Q&A pair | JSON scores + `signal` |
| **AI Career Coach** | Final report | Full session | Markdown report |

### Evaluator signals

| Signal | Interviewer behavior |
|--------|---------------------|
| `advance` | Next competency / harder question |
| `probe` | Targeted follow-up |
| `simplify` | Rephrase or reduce complexity |
| `wrap_up` | Close interview (after min turns) |

## Orchestration Flow (one turn)

1. Candidate submits answer → `POST /session/{id}/turn`
2. **Evaluator** runs → scores + `signal`
3. Orchestrator checks wrap (`signal=wrap_up` + ≥5 turns, or ≥7 turns)
4. **Interviewer** receives `signal` + last evaluation → next question (plain text)
5. On complete → **Coach** generates report → redirect to `/feedback/[id]`

## API Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/session/start` | Strategist + first question |
| POST | `/session/{id}/turn` | Answer → evaluate → next Q |
| GET | `/session/{id}/report` | Coach markdown report |
| GET | `/session/{id}/history` | Full transcript + evals |
| GET | `/sessions` | List sessions |
| DELETE | `/session/{id}` | Delete session |

## Project Structure

```
├── frontend/          # Next.js 14
├── backend/
│   ├── agents/        # 4 agent implementations
│   ├── routers/       # FastAPI routes
│   ├── services/      # orchestrator, prompt_loader
│   ├── state/         # Pydantic models
│   ├── db/            # SQLite
│   └── utils/         # LLM client
├── prompts/           # strategist.md, interviewer.md, ...
├── examples/          # 3 sample transcripts
└── docs/
```

## Design Decisions

1. **Signal-based loop** — Evaluator output directly drives Interviewer; real coordination, not blind chaining.
2. **Plain-text Interviewer** — Feels human; JSON only where structure is required.
3. **Prompts in `prompts/*.md`** — Versioned, reviewable; never embedded in Python.
4. **SQLite** — Zero-config persistence for demos and history.
5. **Mock LLM mode** — Full flow without API costs for reviewers.
6. **No static question arrays** — Mock uses contextual templates keyed by turn/signal only for offline demo.

## Tradeoffs

- Single-process orchestrator (no Redis/queue) — simpler, sufficient for MVP.
- Mock interviewer uses turn/signal heuristics — live OpenAI mode is fully generative.
- No auth — add JWT/NextAuth for production SaaS.

## Example Transcripts

- [Strong candidate](examples/transcript_strong_candidate.md)
- [Weak candidate](examples/transcript_weak_candidate.md)
- [Edge cases](examples/transcript_edge_case.md)

## Future Improvements

- WebSocket streaming for interviewer tokens
- Voice (STT/TTS) mode
- RAG over job descriptions
- PDF export
- Horizontal scaling with Redis session store

---

Built for AI engineering internship excellence — genuine multi-agent orchestration, not a chatbot.
