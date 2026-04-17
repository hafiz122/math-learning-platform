import { Card } from "../common/Card";
import type { Question } from "../../types/question";

interface QuestionCardProps {
  question: Question | null;
}

export function QuestionCard({ question }: QuestionCardProps) {
  if (!question) {
    return (
      <Card className="min-h-[220px]">
        <p className="text-slate-400">Choose a module and load a question to begin.</p>
      </Card>
    );
  }

  return (
    <Card className="min-h-[220px]">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-medium uppercase tracking-wide text-slate-300">
          {question.module.replace("-", " ")}
        </span>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-medium uppercase tracking-wide text-slate-300">
          {question.difficulty}
        </span>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-medium uppercase tracking-wide text-slate-300">
          {question.question_kind.replaceAll("_", " ")}
        </span>
      </div>

      <h2 className="mb-4 text-2xl font-semibold leading-snug text-white">{question.prompt}</h2>

      {question.input_type === "multiple_choice" && question.choices?.length ? (
        <div className="grid gap-3">
          {question.choices.map((choice) => (
            <div key={choice.key} className="rounded-2xl border border-slate-800 bg-slate-950 px-4 py-3 text-slate-300">
              <span className="mr-2 font-semibold text-cyan-300">{choice.key}.</span>
              {choice.label}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-slate-400">Enter your answer below. Algebra answers may use x, y, +, -, ^, and brackets.</p>
      )}
    </Card>
  );
}
