"use client";

import Link from "next/link";
import { Brain, History, LayoutDashboard, Mic } from "lucide-react";
import { cn } from "@/utils/cn";

const links = [
  { href: "/", label: "Home" },
  { href: "/setup", label: "Start Interview" },
  { href: "/history", label: "History" },
];

export function Navbar() {
  return (
    <header className="fixed top-0 z-50 w-full border-b border-border/40 bg-background/70 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-accent">
            <Brain className="h-5 w-5 text-white" />
          </div>
          <span className="bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">
            InterviewIQ <span className="text-primary">AI</span>
          </span>
        </Link>
        <nav className="hidden items-center gap-6 md:flex">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="text-sm text-foreground/70 transition hover:text-foreground"
            >
              {l.label}
            </Link>
          ))}
        </nav>
        <Link
          href="/setup"
          className={cn(
            "flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium",
            "shadow-lg shadow-primary/30 transition hover:opacity-90"
          )}
        >
          <Mic className="h-4 w-4" />
          <span className="hidden sm:inline">Start Mock Interview</span>
        </Link>
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-border/40 py-12 text-center text-sm text-foreground/50">
      <p>InterviewIQ AI — Your Personal AI Interview Panel</p>
      <p className="mt-1 flex items-center justify-center gap-4">
        <LayoutDashboard className="inline h-3 w-3" /> Multi-Agent Orchestration
        <History className="inline h-3 w-3" /> Session Memory
      </p>
    </footer>
  );
}
