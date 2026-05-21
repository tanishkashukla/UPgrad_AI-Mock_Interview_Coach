"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Bot, Brain, GraduationCap, Search } from "lucide-react";

const AGENT_ICONS: Record<string, React.ReactNode> = {
  Strategist: <Brain className="h-3.5 w-3.5" />,
  Interviewer: <Bot className="h-3.5 w-3.5" />,
  Evaluator: <Search className="h-3.5 w-3.5" />,
  "Career Coach": <GraduationCap className="h-3.5 w-3.5" />,
};

export function AgentActivity({ agents }: { agents: string[] }) {
  const unique = Array.from(new Set(agents));
  return (
    <div className="flex flex-wrap gap-2">
      <AnimatePresence mode="popLayout">
        {unique.map((name) => (
          <motion.span
            key={name}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex items-center gap-1.5 rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs text-primary"
          >
            {AGENT_ICONS[name.split(" ")[0]] || <Bot className="h-3.5 w-3.5" />}
            {name}
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-primary" />
            </span>
          </motion.span>
        ))}
      </AnimatePresence>
    </div>
  );
}
