import { useCallback, useState } from "react";
import { fetchQuestion } from "../api/questionApi";
import type { Difficulty, ModuleKey, Question } from "../types/question";

export function useFetchQuestion() {
  const [question, setQuestion] = useState<Question | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const loadQuestion = useCallback(async (moduleKey: ModuleKey, difficulty: Difficulty) => {
    setIsLoading(true);
    try {
      const nextQuestion = await fetchQuestion(moduleKey, difficulty);
      setQuestion(nextQuestion);
      return nextQuestion;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    question,
    isLoading,
    setQuestion,
    loadQuestion
  };
}
