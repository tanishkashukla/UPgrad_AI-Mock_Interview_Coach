import type { SessionSetup, TurnEvaluation } from "./types";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const TIMEOUT_MS = 15000;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(`${API}${path}`, {
      ...init,
      signal: controller.signal,
      headers: { "Content-Type": "application/json", ...init?.headers },
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(
        typeof err.detail === "string" ? err.detail : JSON.stringify(err.detail) || "Request failed"
      );
    }
    return res.json();
  } catch (e) {
    if (e instanceof Error && e.name === "AbortError") {
      throw new Error(
        `Request timed out. Is the backend running at ${API}? Run start.ps1 or uvicorn on port 8000.`
      );
    }
    if (e instanceof TypeError) {
      throw new Error(`Cannot reach API at ${API}. Start the backend first.`);
    }
    throw e;
  } finally {
    clearTimeout(timer);
  }
}

export function startSession(setup: SessionSetup) {
  return request<{
    session_id: string;
    first_question: string;
    strategy: Record<string, unknown>;
    turn: number;
    max_turns: number;
    total_questions: number;
    agents_active: string[];
  }>("/session/start", { method: "POST", body: JSON.stringify(setup) });
}

export function submitTurn(sessionId: string, answer: string) {
  return request<{
    session_id: string;
    evaluation: TurnEvaluation;
    live_scores: Record<string, number>;
    signal: string;
    turn: number;
    next_turn?: number;
    next_question: string | null;
    interview_complete: boolean;
    agents_active: string[];
    overall_score: number;
    readiness_label: string;
  }>(`/session/${sessionId}/turn`, {
    method: "POST",
    body: JSON.stringify({ answer }),
  });
}

export function getReport(sessionId: string) {
  return request<{
    session_id: string;
    report_markdown: string;
    overall_score: number;
    readiness_label: string;
    aggregate_scores: Record<string, number>;
  }>(`/session/${sessionId}/report`);
}

export function getSessionHistory(sessionId: string) {
  return request<Record<string, unknown>>(`/session/${sessionId}/history`);
}

export function listSessions() {
  return request<import("./types").SessionListItem[]>("/sessions");
}

export function deleteSession(sessionId: string) {
  return request<{ deleted: boolean }>(`/session/${sessionId}`, { method: "DELETE" });
}
