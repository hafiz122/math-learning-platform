import { apiRequest } from "./client";
import type {
  CreateSessionResponse,
  QuestionResponse,
  SessionSummary,
  SubmitAnswerRequest,
  ValidationResult
} from "../types/api";
import type { Difficulty, ModuleKey } from "../types/question";

export function createSession() {
  return apiRequest<CreateSessionResponse>("/api/v1/sessions", {
    method: "POST"
  });
}

export function fetchQuestion(moduleKey: ModuleKey, difficulty: Difficulty) {
  const params = new URLSearchParams({ module: moduleKey, difficulty });
  return apiRequest<QuestionResponse>(`/api/v1/questions?${params.toString()}`);
}

export function submitAnswer(payload: SubmitAnswerRequest) {
  return apiRequest<ValidationResult>("/api/v1/answers/validate", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function fetchSessionSummary(sessionId: string) {
  return apiRequest<SessionSummary>(`/api/v1/sessions/${sessionId}/summary`);
}
