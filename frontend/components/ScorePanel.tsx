"use client";

import { motion } from "framer-motion";
import type { TurnEvaluation } from "@/lib/types";
import { DIMENSION_LABELS } from "@/lib/types";

export function ScorePanel({
  evaluation,
  liveScores,
}: {
  evaluation: TurnEvaluation | null;
  liveScores: Record<string, number>;
}) {
  if (!evaluation) {
    return (
      <div className="glass rounded-2xl p-5">
        <h3 className="text-sm font-medium text-white/60">Live Scores</h3>
        <p className="mt-3 text-xs text-white/40">Submit an answer to see real-time evaluation.</p>
      </div>
    );
  }

  const avg =
    Object.values(liveScores).length > 0
      ? Object.values(liveScores).reduce((a, b) => a + b, 0) / Object.values(liveScores).length
      : 0;

  return (
    <div className="glass rounded-2xl p-5">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium">Live Scores</h3>
        <span className="rounded-full bg-indigo-500/20 px-2 py-0.5 text-xs capitalize text-indigo-300">
          {evaluation.signal.replace("_", " ")}
        </span>
      </div>
      <p className="mt-2 text-3xl font-bold text-white">
        {avg.toFixed(1)}
        <span className="text-sm font-normal text-white/40"> / 10 avg</span>
      </p>
      <div className="mt-4 space-y-2">
        {Object.entries(evaluation.scores).map(([k, v]) => (
          <div key={k}>
            <div className="flex justify-between text-xs text-white/50">
              <span>{DIMENSION_LABELS[k] || k}</span>
              <span>{v.toFixed(1)}</span>
            </div>
            <div className="mt-0.5 h-1 overflow-hidden rounded-full bg-white/5">
              <motion.div
                className="h-full bg-gradient-to-r from-indigo-500 to-violet-500"
                initial={{ width: 0 }}
                animate={{ width: `${(v / 10) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
      {evaluation.improvement_tip && (
        <p className="mt-4 rounded-lg border border-white/10 bg-white/5 p-3 text-xs text-white/70">
          {evaluation.improvement_tip}
        </p>
      )}
    </div>
  );
}
