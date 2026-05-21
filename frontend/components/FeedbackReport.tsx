"use client";

export function FeedbackReport({ markdown }: { markdown: string }) {
  const lines = markdown.split("\n");
  return (
    <article className="prose prose-invert max-w-none text-sm leading-relaxed">
      {lines.map((line, i) => {
        if (line.startsWith("# "))
          return (
            <h2 key={i} className="mb-2 mt-6 text-xl font-bold text-white">
              {line.slice(2)}
            </h2>
          );
        if (line.startsWith("## "))
          return (
            <h3 key={i} className="mb-2 mt-4 text-lg font-semibold text-indigo-300">
              {line.slice(3)}
            </h3>
          );
        if (line.startsWith("### "))
          return (
            <h4 key={i} className="mt-3 font-medium text-white/80">
              {line.slice(4)}
            </h4>
          );
        if (line.startsWith("- "))
          return (
            <li key={i} className="ml-4 list-disc text-white/75">
              {line.slice(2)}
            </li>
          );
        if (line.startsWith("|") && line.includes("---")) return null;
        if (line.startsWith("|"))
          return (
            <p key={i} className="font-mono text-xs text-white/50">
              {line}
            </p>
          );
        if (line.trim())
          return (
            <p key={i} className="text-white/75">
              {line}
            </p>
          );
        return <br key={i} />;
      })}
    </article>
  );
}
