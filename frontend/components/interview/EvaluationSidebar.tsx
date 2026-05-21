"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { TurnEvaluation } from "@/types/interview";

export function EvaluationSidebar({
  evaluation,
  aggregateScores,
}: {
  evaluation?: TurnEvaluation | null;
  aggregateScores?: Record<string, number>;
}) {
  if (!evaluation) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle className="text-sm text-foreground/60">Live Evaluation</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-foreground/50">Answer a question to see real-time scoring.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full overflow-hidden">
      <CardHeader>
        <CardTitle className="flex items-center justify-between text-sm">
          Live Evaluation
          <span className="rounded-full bg-primary/20 px-2 py-0.5 text-xs text-primary">
            Turn {evaluation.overall_turn_score?.toFixed?.(1) ?? evaluation.overall_turn_score}/10
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4 text-sm">
        <div>
          <span className="text-xs uppercase tracking-wider text-foreground/40">Quality</span>
          <p className="capitalize text-accent">{evaluation.answer_quality}</p>
        </div>
        {evaluation.strengths?.length > 0 && (
          <div>
            <span className="text-xs text-emerald-400/80">Strengths</span>
            <ul className="mt-1 list-inside list-disc text-foreground/80">
              {evaluation.strengths.slice(0, 3).map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>
        )}
        {evaluation.weaknesses?.length > 0 && (
          <div>
            <span className="text-xs text-amber-400/80">Weaknesses</span>
            <ul className="mt-1 list-inside list-disc text-foreground/70">
              {evaluation.weaknesses.slice(0, 3).map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>
        )}
        {evaluation.improvement_tips?.[0] && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="rounded-lg border border-border/50 bg-muted/50 p-3 text-xs text-foreground/70"
          >
            💡 {evaluation.improvement_tips[0]}
          </motion.div>
        )}
        {aggregateScores && Object.keys(aggregateScores).length > 0 && (
          <div className="border-t border-border/40 pt-3">
            <span className="text-xs text-foreground/40">Session Average</span>
            <p className="text-2xl font-bold text-primary">
              {(
                Object.values(aggregateScores).reduce((a, b) => a + b, 0) /
                Object.values(aggregateScores).length
              ).toFixed(1)}
              <span className="text-sm font-normal text-foreground/50"> / 10</span>
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
