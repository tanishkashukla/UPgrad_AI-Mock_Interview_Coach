"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Bot, Brain, GraduationCap, Search } from "lucide-react";

const ICONS: Record<string, React.ReactNode> = {
  Profile: <Brain className="h-3 w-3" />,
  Strategist: <Brain className="h-3 w-3" />,
  Interviewer: <Bot className="h-3 w-3" />,
  Evaluator: <Search className="h-3 w-3" />,
  Coach: <GraduationCap className="h-3 w-3" />,
  Career: <GraduationCap className="h-3 w-3" />,
};

function iconFor(name: string) {
  for (const [k, v] of Object.entries(ICONS)) {
    if (name.includes(k)) return v;
  }
  return <Bot className="h-3 w-3" />;
}

export function AgentActivity({ agents }: { agents: string[] }) {
  const unique = Array.from(new Set(agents));
  return (
    <div className="flex flex-wrap gap-2">
      <AnimatePresence mode="popLayout">
        {unique.map((name) => (
          <motion.span
            key={name}
            layout
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex items-center gap-1.5 rounded-full border border-indigo-500/30 bg-indigo-500/10 px-2.5 py-1 text-xs text-indigo-300"
          >
            {iconFor(name)}
            {name}
            <span className="relative flex h-1.5 w-1.5">
              <span className="absolute h-full w-full animate-ping rounded-full bg-indigo-400 opacity-75" />
              <span className="relative h-1.5 w-1.5 rounded-full bg-indigo-400" />
            </span>
          </motion.span>
        ))}
      </AnimatePresence>
    </div>
  );
}
