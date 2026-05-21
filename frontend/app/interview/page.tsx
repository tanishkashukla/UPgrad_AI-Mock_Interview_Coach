"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2, Send } from "lucide-react";
import { AgentActivity } from "@/components/AgentActivity";
import { InterviewChat } from "@/components/InterviewChat";
import { ScorePanel } from "@/components/ScorePanel";
import { TurnCounter } from "@/components/TurnCounter";
import { getSessionHistory, submitTurn } from "@/lib/api";
import { normalizeQuestion } from "@/lib/sanitize";
import type { TranscriptTurn, TurnEvaluation } from "@/lib/types";

function mapServerTurns(raw: Array<{ role: string; content: string; turn?: number }>): TranscriptTurn[] {
  return raw.map((t) => ({
    role: t.role,
    content: t.role === "interviewer" ? normalizeQuestion(t.content) : t.content,
    turn: t.turn ?? 1,
  }));
}

export default function InterviewPage() {
  const router = useRouter();
  const [sessionId, setSessionId] = useState("");
  const [totalQuestions, setTotalQuestions] = useState(5);
  const [turn, setTurn] = useState(1);
  const [turns, setTurns] = useState<TranscriptTurn[]>([]);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [initLoading, setInitLoading] = useState(true);
  const [typing, setTyping] = useState(false);
  const [agents, setAgents] = useState<string[]>([]);
  const [evaluation, setEvaluation] = useState<TurnEvaluation | null>(null);
  const [liveScores, setLiveScores] = useState<Record<string, number>>({});
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      const raw = sessionStorage.getItem("pilot_session");
      if (!raw) {
        router.replace("/setup");
        return;
      }
      const data = JSON.parse(raw);
      const sid = data.sessionId as string;
      setSessionId(sid);
      setTotalQuestions(data.maxTurns ?? 5);

      try {
        const server = await getSessionHistory(sid);
        const serverTurns = server.turns as Array<{ role: string; content: string; turn?: number }>;
        if (serverTurns?.length) {
          const mapped = mapServerTurns(serverTurns);
          setTurns(mapped);
          const last = mapped[mapped.length - 1];
          setTurn(last.turn);
        } else {
          setTurns([
            {
              role: "interviewer",
              content: normalizeQuestion(data.firstQuestion as string),
              turn: 1,
            },
          ]);
        }
        if (server.current_turn) {
          setTurn(server.current_turn as number);
        }
      } catch {
        setTurns([
          {
            role: "interviewer",
            content: normalizeQuestion(data.firstQuestion as string),
            turn: 1,
          },
        ]);
      }
      setAgents(["Profile Strategist", "Interviewer"]);
      setInitLoading(false);
    }
    load();
  }, [router]);

  const send = useCallback(async () => {
    const text = answer.trim();
    if (!text || !sessionId) return;
    setLoading(true);
    setError("");
    setAnswer("");
    setTurns((t) => [...t, { role: "candidate", content: text, turn }]);
    setTyping(true);
    setAgents(["Real-Time Evaluator", "Interviewer"]);

    try {
      const res = await submitTurn(sessionId, text);
      setEvaluation(res.evaluation);
      setLiveScores(res.live_scores);
      setAgents(res.agents_active);

      if (res.interview_complete) {
        setTyping(false);
        router.push(`/feedback/${sessionId}`);
        return;
      }

      setTimeout(() => {
        setTyping(false);
        if (res.next_question) {
          const nt = res.next_turn ?? turn + 1;
          setTurn(nt);
          setTurns((t) => [
            ...t,
            { role: "interviewer", content: normalizeQuestion(res.next_question!), turn: nt },
          ]);
        }
      }, 700);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error");
      setTyping(false);
    } finally {
      setLoading(false);
    }
  }, [answer, sessionId, turn, router]);

  if (initLoading || !sessionId) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-indigo-400" />
      </div>
    );
  }

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-8 lg:flex-row">
      <div className="flex min-h-[70vh] flex-1 flex-col">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <AgentActivity agents={agents} />
          <TurnCounter
            current={Math.min(turn, totalQuestions)}
            total={totalQuestions}
          />
        </div>
        <div className="glass flex flex-1 flex-col rounded-2xl p-4">
          <InterviewChat turns={turns} typing={typing} />
          {error && <p className="text-sm text-red-400">{error}</p>}
          <div className="mt-4 flex gap-2 border-t border-white/[0.06] pt-4">
            <textarea
              className="min-h-[72px] flex-1 resize-none rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Your answer... (Shift+Enter for newline)"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  send();
                }
              }}
              disabled={loading}
            />
            <button
              onClick={send}
              disabled={loading || !answer.trim()}
              className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-600 disabled:opacity-40"
            >
              {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Send className="h-5 w-5" />}
            </button>
          </div>
        </div>
      </div>
      <aside className="w-full lg:w-72">
        <ScorePanel evaluation={evaluation} liveScores={liveScores} />
      </aside>
    </div>
  );
}
