"use client";

import {
  Radar,
  RadarChart as RechartsRadar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";
import { DIMENSION_LABELS } from "@/lib/types";

export function RadarChart({ scores }: { scores: Record<string, number> }) {
  const data = Object.entries(scores).map(([k, v]) => ({
    dimension: DIMENSION_LABELS[k] || k,
    score: v,
  }));
  if (!data.length) return null;
  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsRadar data={data}>
        <PolarGrid stroke="rgba(255,255,255,0.1)" />
        <PolarAngleAxis dataKey="dimension" tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 10 }} />
        <PolarRadiusAxis domain={[0, 10]} tick={{ fill: "rgba(255,255,255,0.3)" }} />
        <Radar
          dataKey="score"
          stroke="#6366F1"
          fill="#8B5CF6"
          fillOpacity={0.35}
        />
      </RechartsRadar>
    </ResponsiveContainer>
  );
}
