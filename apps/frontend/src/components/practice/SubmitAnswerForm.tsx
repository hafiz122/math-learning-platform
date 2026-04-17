import { useEffect, useState, type FormEvent } from "react";
import { Button } from "../common/Button";
import { Input } from "../common/Input";
import type { Question } from "../../types/question";

interface SubmitAnswerFormProps {
  question: Question | null;
  isSubmitting: boolean;
  onSubmit: (answer: string) => Promise<void> | void;
}

export function SubmitAnswerForm({ question, isSubmitting, onSubmit }: SubmitAnswerFormProps) {
  const [answer, setAnswer] = useState("");

  useEffect(() => {
    setAnswer("");
  }, [question?.question_id]);

  if (!question) {
    return null;
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!answer.trim()) {
      return;
    }
    await onSubmit(answer);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {question.input_type === "multiple_choice" ? (
        <div className="grid gap-2 sm:grid-cols-2">
          {question.choices?.map((choice) => (
            <button
              key={choice.key}
              type="button"
              onClick={() => setAnswer(choice.key)}
              className={[
                "rounded-2xl border px-4 py-3 text-left text-sm transition",
                answer === choice.key
                  ? "border-cyan-500 bg-cyan-500/10 text-cyan-300"
                  : "border-slate-800 bg-slate-900 text-slate-300 hover:text-white"
              ].join(" ")}
            >
              <span className="mr-2 font-semibold">{choice.key}.</span>
              {choice.label}
            </button>
          ))}
        </div>
      ) : (
        <Input
          value={answer}
          onChange={(event) => setAnswer(event.target.value)}
          placeholder={question.placeholder ?? "Type your answer"}
          aria-label="Answer input"
        />
      )}

      <Button type="submit" disabled={isSubmitting || !answer.trim()}>
        {isSubmitting ? "Checking..." : "Submit answer"}
      </Button>
    </form>
  );
}
