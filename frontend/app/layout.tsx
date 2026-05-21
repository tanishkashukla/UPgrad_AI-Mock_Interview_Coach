import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import { Plane } from "lucide-react";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "InterviewPilot AI — Practice smarter. Interview better.",
  description: "Multi-agent adaptive mock interviews with real-time evaluation.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <header className="fixed top-0 z-50 w-full border-b border-white/[0.06] bg-[#0a0a0f]/80 backdrop-blur-xl">
          <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
            <Link href="/" className="flex items-center gap-2 font-semibold">
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600">
                <Plane className="h-4 w-4 text-white" />
              </span>
              InterviewPilot <span className="text-indigo-400">AI</span>
            </Link>
            <nav className="hidden gap-6 text-sm text-white/60 md:flex">
              <Link href="/" className="hover:text-white">Home</Link>
              <Link href="/setup" className="hover:text-white">Start</Link>
              <Link href="/history" className="hover:text-white">History</Link>
            </nav>
            <Link
              href="/setup"
              className="rounded-lg bg-gradient-to-r from-indigo-600 to-violet-600 px-4 py-2 text-sm font-medium shadow-lg shadow-indigo-500/25 hover:opacity-90"
            >
              Start Interview
            </Link>
          </div>
        </header>
        <main className="min-h-screen pt-14">{children}</main>
        <footer className="border-t border-white/[0.06] py-8 text-center text-xs text-white/40">
          InterviewPilot AI — Multi-agent orchestration · Practice smarter. Interview better.
        </footer>
      </body>
    </html>
  );
}
