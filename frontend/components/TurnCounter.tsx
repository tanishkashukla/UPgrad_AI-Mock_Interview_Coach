"use client";

import { motion } from "framer-motion";

/** Progress for interview questions (not internal agent turns). */
export function TurnCounter({
  current,
  total,
}: {
  current: number;
  total: number;
}) {
  const pct = Math.min(100, (current / total) * 100);
  return (
    <div className="text-right">
      <p className="text-xs text-white/50">
        Question{" "}
        <span className="font-mono text-indigo-400">{current}</span> of {total}
      </p>
      <div className="mt-1.5 h-1.5 w-32 overflow-hidden rounded-full bg-white/5">
        <motion.div
          className="h-full bg-gradient-to-r from-indigo-500 to-violet-500"
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.4 }}
        />
      </div>
    </div>
  );
}
