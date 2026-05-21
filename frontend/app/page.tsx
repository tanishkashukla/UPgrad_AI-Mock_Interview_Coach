"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, BarChart3, Bot, Brain, Sparkles, Target, Zap } from "lucide-react";

const agents = [
  { name: "Profile Strategist", icon: Brain, desc: "Plans competencies, difficulty, and probing strategy before you start." },
  { name: "Interviewer", icon: Bot, desc: "Adaptive dialogue — never a static question list." },
  { name: "Real-Time Evaluator", icon: Target, desc: "Scores every answer and signals advance, probe, simplify, or wrap up." },
  { name: "AI Career Coach", icon: Sparkles, desc: "Full markdown report with roadmap and resources." },
];

export default function LandingPage() {
  return (
    <div>
      <section className="relative px-4 pb-24 pt-20 text-center sm:px-6">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
          <p className="mb-4 inline-block rounded-full border border-indigo-500/30 bg-indigo-500/10 px-4 py-1 text-sm text-indigo-300">
            4-agent orchestration · Not a chatbot
          </p>
          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
            <span className="gradient-text">InterviewPilot AI</span>
          </h1>
          <p className="mx-auto mt-4 max-w-xl text-lg text-white/60">
            Practice smarter. Interview better.
          </p>
          <p className="mx-auto mt-2 max-w-2xl text-white/45">
            Realistic 5–7 turn adaptive interviews with live scoring, signal-driven probing, and
            recruiter-grade feedback.
          </p>
          <Link
            href="/setup"
            className="mt-8 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 px-8 py-3 font-medium shadow-xl shadow-indigo-500/30 hover:opacity-90"
          >
            Start Mock Interview <ArrowRight className="h-4 w-4" />
          </Link>
        </motion.div>

        <motion.div
          className="mx-auto mt-16 grid max-w-4xl gap-4 sm:grid-cols-2 lg:grid-cols-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          {agents.map((a, i) => (
            <motion.div
              key={a.name}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * i }}
              className="glass glow rounded-2xl p-5 text-left"
            >
              <a.icon className="h-8 w-8 text-indigo-400" />
              <h3 className="mt-3 font-semibold">{a.name}</h3>
              <p className="mt-1 text-xs text-white/50">{a.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      <section className="border-y border-white/[0.06] bg-[#111118]/50 py-16">
        <div className="mx-auto grid max-w-4xl gap-8 px-4 sm:grid-cols-3">
          {[
            { icon: Zap, t: "Adaptive AI", d: "Evaluator signals drive the next question." },
            { icon: BarChart3, t: "Live analytics", d: "Six-dimension radar and readiness labels." },
            { icon: Target, t: "STAR-aware", d: "Structure and depth scored every turn." },
          ].map((f) => (
            <div key={f.t} className="text-center">
              <f.icon className="mx-auto h-8 w-8 text-violet-400" />
              <h3 className="mt-3 font-medium">{f.t}</h3>
              <p className="mt-1 text-sm text-white/45">{f.d}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
