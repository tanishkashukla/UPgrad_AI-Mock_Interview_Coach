export type InterviewType =
  | "behavioral"
  | "technical"
  | "mixed"
  | "system_design"
  | "leadership";

export type Difficulty = "easy" | "medium" | "hard" | "adaptive";
export type ExperienceLevel = "intern" | "junior" | "mid" | "senior" | "lead";

export interface SessionSetup {
  target_role: string;
  resume_snippet: string;
  interview_type: InterviewType;
  difficulty: Difficulty;
  experience_level: ExperienceLevel;
}

export interface TurnEvaluation {
  scores: Record<string, number>;
  overall_turn_score: number;
  star_analysis?: Record<string, unknown>;
  answer_quality: string;
  strengths: string[];
  weaknesses: string[];
  missed_opportunities: string[];
  better_sample_answer: string;
  improvement_tips: string[];
  interviewer_hints?: Record<string, unknown>;
}

export interface TranscriptMessage {
  role: string;
  content: string;
  turn_number: number;
  timestamp?: string;
}

export interface InterviewSession {
  session_id: string;
  setup: SessionSetup;
  strategy?: Record<string, unknown>;
  status: string;
  current_turn: number;
  transcript: TranscriptMessage[];
  evaluations: TurnEvaluation[];
  latest_evaluator_feedback?: TurnEvaluation;
  current_question?: string;
  final_report_markdown?: string;
  aggregate_scores: Record<string, number>;
  overall_score: number;
}

export const SCORE_DIMENSIONS = [
  "communication",
  "technical_depth",
  "clarity",
  "structure",
  "confidence",
  "leadership",
  "relevance",
  "critical_thinking",
  "problem_solving",
] as const;

export const DIMENSION_LABELS: Record<string, string> = {
  communication: "Communication",
  technical_depth: "Technical Depth",
  clarity: "Clarity",
  structure: "Structure",
  confidence: "Confidence",
  leadership: "Leadership",
  relevance: "Relevance",
  critical_thinking: "Critical Thinking",
  problem_solving: "Problem Solving",
};
