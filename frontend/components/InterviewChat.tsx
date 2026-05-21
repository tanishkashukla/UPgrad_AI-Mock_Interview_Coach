"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { TranscriptTurn } from "@/lib/types";

function TypingDots() {
  return (
    <div className="flex gap-1 rounded-2xl rounded-bl-md glass px-4 py-3">
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          className="h-2 w-2 rounded-full bg-indigo-400"
          animate={{ y: [0, -5, 0] }}
          transition={{ repeat: Infinity, duration: 0.5, delay: i * 0.12 }}
        />
      ))}
    </div>
  );
}

export function InterviewChat({
  turns,
  typing,
}: {
  turns: TranscriptTurn[];
  typing: boolean;
}) {
  const end = useRef<HTMLDivElement>(null);
  useEffect(() => {
    end.current?.scrollIntoView({ behavior: "smooth" });
  }, [turns, typing]);

  return (
    <div className="flex-1 space-y-4 overflow-y-auto pr-1">
      <AnimatePresence>
        {turns.map((t, i) => (
          <motion.div
            key={`${t.turn}-${t.role}-${i}`}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex ${t.role === "candidate" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[88%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                t.role === "candidate"
                  ? "rounded-br-md bg-gradient-to-br from-indigo-600 to-violet-600 text-white shadow-lg shadow-indigo-500/20"
                  : "glass rounded-bl-md text-white/90"
              }`}
            >
              {t.content}
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
      {typing && (
        <div className="flex justify-start">
          <TypingDots />
        </div>
      )}
      <div ref={end} />
    </div>
  );
}
