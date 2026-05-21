"use client";

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import { DIMENSION_LABELS } from "@/types/interview";

export function ScoreRadar({ scores }: { scores: Record<string, number> }) {
  const data = Object.entries(scores).map(([key, value]) => ({
    dimension: DIMENSION_LABELS[key] || key,
    score: value,
    fullMark: 10,
  }));

  if (!data.length) return null;

  return (
    <ResponsiveContainer width="100%" height={320}>
      <RadarChart data={data}>
        <PolarGrid stroke="hsl(217 33% 25%)" />
        <PolarAngleAxis dataKey="dimension" tick={{ fill: "hsl(210 40% 70%)", fontSize: 10 }} />
        <PolarRadiusAxis angle={30} domain={[0, 10]} tick={{ fill: "hsl(210 40% 50%)" }} />
        <Radar
          name="Score"
          dataKey="score"
          stroke="hsl(262 83% 58%)"
          fill="hsl(262 83% 58%)"
          fillOpacity={0.4}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
}
