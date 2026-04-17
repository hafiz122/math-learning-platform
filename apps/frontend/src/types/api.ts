import type { Difficulty, ModuleKey, Question } from "./question";

export interface CreateSessionResponse {
  session_id: string;
}

export interface QuestionResponse extends Question {}

export interface SubmitAnswerRequest {
  session_id?: string;
  module: ModuleKey;
  difficulty: Difficulty;
  question_id: string;
  validation_token: string;
  user_answer: string;
}

export interface SessionSummary {
  session_id: string;
  attempts: number;
  correct_attempts: number;
  accuracy: number;
}

export interface ValidationResult {
  attempt_id?: string;
  session_id?: string;
  is_correct: boolean;
  normalized_user_answer: string;
  correct_answer: string;
  explanation: string;
  session_summary?: SessionSummary;
}
