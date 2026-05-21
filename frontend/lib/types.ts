export type InterviewType = "behavioral" | "technical" | "case" | "mixed";
export type ExperienceLevel = "student" | "0-2" | "2-5" | "5+";
export type EvalSignal = "advance" | "probe" | "simplify" | "wrap_up";

export interface SessionSetup {
  target_role: string;
  background: string;
  interview_type: InterviewType;
  experience_level: ExperienceLevel;
}

export interface TurnEvaluation {
  turn: number;
  scores: Record<string, number>;
  strengths: string[];
  weaknesses: string[];
  improvement_tip: string;
  signal: EvalSignal;
}

export const SCORE_DIMENSIONS = [
  "communication",
  "technical_depth",
  "structure",
  "relevance",
  "confidence",
  "problem_solving",
] as const;

export const DIMENSION_LABELS: Record<string, string> = {
  communication: "Communication",
  technical_depth: "Technical Depth",
  structure: "Structure",
  relevance: "Relevance",
  confidence: "Confidence",
  problem_solving: "Problem Solving",
};

export interface TranscriptTurn {
  role: string;
  content: string;
  turn: number;
  ts?: string;
}

export interface SessionListItem {
  session_id: string;
  target_role: string;
  interview_type: string;
  status: string;
  overall_score: number;
  readiness: string;
  turn_count: number;
  created_at: string | null;
}
