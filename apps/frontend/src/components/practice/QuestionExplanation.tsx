import { Card } from "../common/Card";
import type { ValidationResult } from "../../types/api";

interface QuestionExplanationProps {
  result: ValidationResult | null;
}

export function QuestionExplanation({ result }: QuestionExplanationProps) {
  if (!result) {
    return null;
  }

  return (
    <Card className={result.is_correct ? "border-emerald-700/60" : "border-rose-700/60"}>
      <div className="mb-3 flex items-center gap-3">
        <span
          className={[
            "rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide",
            result.is_correct ? "bg-emerald-500/15 text-emerald-300" : "bg-rose-500/15 text-rose-300"
          ].join(" ")}
        >
          {result.is_correct ? "Correct" : "Not correct"}
        </span>
      </div>

      <p className="mb-2 text-sm text-slate-300">Your answer: {result.normalized_user_answer || "—"}</p>
      <p className="mb-4 text-sm text-slate-300">Correct answer: {result.correct_answer}</p>
      <p className="text-slate-200">{result.explanation}</p>
    </Card>
  );
}
