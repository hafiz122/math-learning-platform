import { useState } from "react";
import { submitAnswer } from "../api/questionApi";
import type { SubmitAnswerRequest, ValidationResult } from "../types/api";

export function useSubmitAnswer() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<ValidationResult | null>(null);

  async function handleSubmit(payload: SubmitAnswerRequest) {
    setIsSubmitting(true);
    try {
      const response = await submitAnswer(payload);
      setResult(response);
      return response;
    } finally {
      setIsSubmitting(false);
    }
  }

  return {
    isSubmitting,
    result,
    setResult,
    handleSubmit
  };
}
