"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";
import { startSession } from "@/lib/api";
import { normalizeQuestion } from "@/lib/sanitize";
import type { ExperienceLevel, InterviewType } from "@/lib/types";

const ROLES = ["Software Engineer", "Product Manager", "Data Analyst", "ML Engineer", "Designer"];
const TYPES: { v: InterviewType; l: string }[] = [
  { v: "mixed", l: "Mixed" },
  { v: "behavioral", l: "Behavioral" },
  { v: "technical", l: "Technical" },
  { v: "case", l: "Case" },
];
const LEVELS: { v: ExperienceLevel; l: string }[] = [
  { v: "student", l: "Student" },
  { v: "0-2", l: "0–2 years" },
  { v: "2-5", l: "2–5 years" },
  { v: "5+", l: "5+ years" },
];

export default function SetupPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    target_role: "",
    background: "",
    interview_type: "mixed" as InterviewType,
    experience_level: "2-5" as ExperienceLevel,
  });

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.target_role.trim()) {
      setError("Enter a target role.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await startSession(form);
      const question = normalizeQuestion(res.first_question);
      sessionStorage.setItem(
        "pilot_session",
        JSON.stringify({
          sessionId: res.session_id,
          firstQuestion: question,
          maxTurns: res.total_questions ?? res.max_turns ?? 5,
          setup: form,
        })
      );
      router.push("/interview");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-xl px-4 py-12">
      <h1 className="text-2xl font-bold">Interview Setup</h1>
      <p className="mt-1 text-sm text-white/50">Profile Strategist will plan your session.</p>
      <form onSubmit={onSubmit} className="glass mt-8 space-y-5 rounded-2xl p-6">
        <div>
          <label className="text-sm text-white/70">Target role *</label>
          <input
            className="mt-1.5 w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.target_role}
            onChange={(e) => setForm({ ...form, target_role: e.target.value })}
            placeholder="e.g. Senior Product Manager — B2B SaaS"
          />
          <div className="mt-2 flex flex-wrap gap-2">
            {ROLES.map((r) => (
              <button
                key={r}
                type="button"
                onClick={() => setForm({ ...form, target_role: r })}
                className="rounded-full border border-white/10 px-2.5 py-0.5 text-xs text-white/50 hover:border-indigo-500/50"
              >
                {r}
              </button>
            ))}
          </div>
        </div>
        <div>
          <label className="text-sm text-white/70">Background (optional)</label>
          <textarea
            className="mt-1.5 min-h-[120px] w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 outline-none focus:ring-2 focus:ring-indigo-500"
            value={form.background}
            onChange={(e) => setForm({ ...form, background: e.target.value })}
            placeholder="Resume snippet, projects, skills..."
          />
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label className="text-sm text-white/70">Interview type</label>
            <select
              className="mt-1.5 w-full rounded-lg border border-white/10 bg-[#111118] px-3 py-2.5"
              value={form.interview_type}
              onChange={(e) => setForm({ ...form, interview_type: e.target.value as InterviewType })}
            >
              {TYPES.map((t) => (
                <option key={t.v} value={t.v}>{t.l}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-sm text-white/70">Experience</label>
            <select
              className="mt-1.5 w-full rounded-lg border border-white/10 bg-[#111118] px-3 py-2.5"
              value={form.experience_level}
              onChange={(e) => setForm({ ...form, experience_level: e.target.value as ExperienceLevel })}
            >
              {LEVELS.map((l) => (
                <option key={l.v} value={l.v}>{l.l}</option>
              ))}
            </select>
          </div>
        </div>
        {error && <p className="text-sm text-red-400">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 py-3 font-medium disabled:opacity-50"
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
          {loading ? "Starting interview…" : "Begin Interview"}
        </button>
      </form>
    </div>
  );
}
