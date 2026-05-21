"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { Download, Loader2 } from "lucide-react";
import { FeedbackReport } from "@/components/FeedbackReport";
import { RadarChart } from "@/components/RadarChart";
import { getReport, getSessionHistory } from "@/lib/api";

export default function FeedbackPage() {
  const { id } = useParams();
  const sessionId = id as string;
  const [loading, setLoading] = useState(true);
  const [report, setReport] = useState("");
  const [score, setScore] = useState(0);
  const [readiness, setReadiness] = useState("");
  const [scores, setScores] = useState<Record<string, number>>({});
  const [evaluations, setEvaluations] = useState<Array<Record<string, unknown>>>([]);
  const [turns, setTurns] = useState<Array<Record<string, unknown>>>([]);
  const [openSample, setOpenSample] = useState<number | null>(0);

  useEffect(() => {
    Promise.all([getReport(sessionId), getSessionHistory(sessionId)])
      .then(([r, h]) => {
        setReport(r.report_markdown);
        setScore(r.overall_score);
        setReadiness(r.readiness_label);
        setScores(r.aggregate_scores);
        setEvaluations((h.evaluations as Array<Record<string, unknown>>) || []);
        setTurns((h.turns as Array<Record<string, unknown>>) || []);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [sessionId]);

  function exportMd() {
    const blob = new Blob([report], { type: "text/markdown" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `interviewpilot-${sessionId.slice(0, 8)}.md`;
    a.click();
  }

  const strengths = Array.from(
    new Set(evaluations.flatMap((e) => (e.strengths as string[]) || []))
  ).slice(0, 3);
  const gaps = Array.from(
    new Set(evaluations.flatMap((e) => (e.weaknesses as string[]) || []))
  ).slice(0, 3);
  const samples = evaluations
    .filter((e) => e.improvement_tip)
    .slice(0, 3)
    .map((e, i) => ({ q: `Turn ${e.turn}`, tip: e.improvement_tip as string }));

  if (loading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-indigo-400" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">Feedback Dashboard</h1>
            <p className="text-white/50">Session {sessionId.slice(0, 8)}…</p>
          </div>
          <button
            onClick={exportMd}
            className="flex items-center gap-2 rounded-lg border border-white/10 px-4 py-2 text-sm hover:bg-white/5"
          >
            <Download className="h-4 w-4" /> Export Report
          </button>
        </div>
      </motion.div>

      <div className="mt-8 grid gap-6 lg:grid-cols-3">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass glow rounded-2xl p-6 text-center lg:col-span-1"
        >
          <p className="text-sm text-white/50">Overall Score</p>
          <p className="mt-2 text-5xl font-bold text-indigo-300">{score.toFixed(0)}</p>
          <p className="mt-2 rounded-full bg-violet-500/20 px-3 py-1 text-sm text-violet-300">
            {readiness || "Interview Ready"}
          </p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="glass rounded-2xl p-4 lg:col-span-2"
        >
          <h2 className="mb-2 text-sm font-medium text-white/60">Skill Radar</h2>
          <RadarChart scores={scores} />
        </motion.div>
      </div>

      <div className="mt-6 grid gap-6 md:grid-cols-2">
        <div className="glass rounded-2xl p-5">
          <h3 className="text-emerald-400">Top Strengths</h3>
          <ul className="mt-3 list-inside list-disc text-sm text-white/75">
            {strengths.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
        <div className="glass rounded-2xl p-5">
          <h3 className="text-amber-400">Top Gaps</h3>
          <ul className="mt-3 list-inside list-disc text-sm text-white/75">
            {gaps.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      </div>

      {samples.length > 0 && (
        <div className="glass mt-6 rounded-2xl p-5">
          <h3 className="font-medium">Better Answers & Tips</h3>
          {samples.map((s, i) => (
            <div key={i} className="mt-3 border-t border-white/[0.06] pt-3 first:border-0 first:pt-0">
              <button
                className="text-left text-sm font-medium text-indigo-300"
                onClick={() => setOpenSample(openSample === i ? null : i)}
              >
                {s.q} {openSample === i ? "▾" : "▸"}
              </button>
              {openSample === i && (
                <p className="mt-2 text-sm text-white/65">{s.tip}</p>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="glass mt-6 rounded-2xl p-5">
        <h3 className="mb-4 font-medium">Transcript</h3>
        <div className="max-h-64 space-y-2 overflow-y-auto text-sm">
          {turns.map((t, i) => (
            <p key={i} className={t.role === "candidate" ? "text-indigo-200" : "text-white/60"}>
              <strong className="capitalize">{String(t.role)}:</strong> {String(t.content)}
            </p>
          ))}
        </div>
      </div>

      <div className="glass mt-6 rounded-2xl p-6">
        <FeedbackReport markdown={report} />
      </div>

      <div className="mt-8 flex gap-3">
        <Link href="/history" className="rounded-lg border border-white/10 px-4 py-2 text-sm">
          History
        </Link>
        <Link
          href="/setup"
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium"
        >
          New Interview
        </Link>
      </div>
    </div>
  );
}
