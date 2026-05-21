"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Trash2, Loader2 } from "lucide-react";
import { deleteSession, listSessions } from "@/lib/api";
import type { SessionListItem } from "@/lib/types";

export default function HistoryPage() {
  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try {
      setSessions(await listSessions());
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function remove(id: string) {
    if (!confirm("Delete this session?")) return;
    await deleteSession(id);
    load();
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="text-2xl font-bold">Session History</h1>
      <p className="text-sm text-white/50">Past mock interviews</p>
      {loading ? (
        <Loader2 className="mx-auto mt-12 h-8 w-8 animate-spin text-indigo-400" />
      ) : sessions.length === 0 ? (
        <p className="mt-8 text-center text-white/40">
          No sessions yet. <Link href="/setup" className="text-indigo-400">Start one</Link>
        </p>
      ) : (
        <ul className="mt-8 space-y-3">
          {sessions.map((s) => (
            <li key={s.session_id} className="glass flex items-center justify-between rounded-xl p-4">
              <Link
                href={s.status === "completed" ? `/feedback/${s.session_id}` : "/setup"}
                className="flex-1"
              >
                <p className="font-medium">{s.target_role || "Interview"}</p>
                <p className="text-xs text-white/45">
                  {s.interview_type} · {s.turn_count} turns ·{" "}
                  {s.created_at ? new Date(s.created_at).toLocaleDateString() : ""}
                  {s.readiness ? ` · ${s.readiness}` : ""}
                </p>
              </Link>
              <div className="flex items-center gap-4">
                {s.status === "completed" && (
                  <span className="text-xl font-bold text-indigo-300">
                    {s.overall_score.toFixed(0)}
                  </span>
                )}
                <button
                  onClick={() => remove(s.session_id)}
                  className="text-white/30 hover:text-red-400"
                  aria-label="Delete"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
