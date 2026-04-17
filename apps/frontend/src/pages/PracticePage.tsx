import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Button } from "../components/common/Button";
import { Loader } from "../components/common/Loader";
import { ModuleTabs } from "../components/practice/ModuleTabs";
import { DifficultySelector } from "../components/practice/DifficultySelector";
import { QuestionCard } from "../components/practice/QuestionCard";
import { SubmitAnswerForm } from "../components/practice/SubmitAnswerForm";
import { QuestionExplanation } from "../components/practice/QuestionExplanation";
import { ScorePanel } from "../components/practice/ScorePanel";
import { fetchSessionSummary } from "../api/questionApi";
import { getAuthMe } from "../api/authApi";
import { useFetchQuestion } from "../hooks/useFetchQuestion";
import { usePracticeSession } from "../hooks/usePracticeSession";
import { useSubmitAnswer } from "../hooks/useSubmitAnswer";
import type { SessionSummary } from "../types/api";
import type { Difficulty, ModuleKey } from "../types/question";

const moduleKeys: ModuleKey[] = [
  "integer-operations",
  "algebra-expressions",
  "algebra-formulas",
];

const FREE_PRACTICE_LIMIT = 12;
const FREE_ATTEMPTS_STORAGE_KEY = "mlp_free_attempts_used";

function getModuleKey(value?: string): ModuleKey {
  return moduleKeys.includes(value as ModuleKey)
    ? (value as ModuleKey)
    : "integer-operations";
}

function readStoredFreeAttempts(): number {
  if (typeof window === "undefined") {
    return 0;
  }

  const raw = window.localStorage.getItem(FREE_ATTEMPTS_STORAGE_KEY);
  const parsed = Number(raw);

  if (!Number.isFinite(parsed) || parsed < 0) {
    return 0;
  }

  return parsed;
}

function writeStoredFreeAttempts(value: number) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(FREE_ATTEMPTS_STORAGE_KEY, String(value));
}

export function PracticePage() {
  const params = useParams();
  const moduleKey = useMemo(() => getModuleKey(params.moduleKey), [params.moduleKey]);

  const [difficulty, setDifficulty] = useState<Difficulty>("easy");
  const [error, setError] = useState("");
  const [sessionSummary, setSessionSummary] = useState<SessionSummary | undefined>(undefined);
  const [freeAttemptsUsed, setFreeAttemptsUsed] = useState<number>(0);
  const [authChecked, setAuthChecked] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const { sessionId, isCreating, startSession } = usePracticeSession();
  const { question, isLoading, loadQuestion } = useFetchQuestion();
  const { isSubmitting, result, setResult, handleSubmit } = useSubmitAnswer();

  useEffect(() => {
    setFreeAttemptsUsed(readStoredFreeAttempts());
  }, []);

  useEffect(() => {
    void getAuthMe()
      .then((me) => {
        setIsAuthenticated(Boolean(me.authenticated));
      })
      .catch(() => {
        setIsAuthenticated(false);
      })
      .finally(() => {
        setAuthChecked(true);
      });
  }, []);

  useEffect(() => {
    void loadQuestion(moduleKey, difficulty).catch((nextError: unknown) => {
      setError(nextError instanceof Error ? nextError.message : "Unable to load question");
    });
  }, [moduleKey, difficulty, loadQuestion]);

  useEffect(() => {
    if (!sessionId) {
      return;
    }

    void fetchSessionSummary(sessionId)
      .then((summary) => {
        setSessionSummary(summary);
      })
      .catch(() => {
        // ignore summary load failure silently
      });
  }, [sessionId]);

  const freePracticeLocked =
    authChecked && !isAuthenticated && freeAttemptsUsed >= FREE_PRACTICE_LIMIT;

  const freeQuestionsRemaining = Math.max(0, FREE_PRACTICE_LIMIT - freeAttemptsUsed);

  const onNewQuestion = async () => {
    if (freePracticeLocked) {
      setError("You have used all 12 free questions. Subscribe or log in with your activation code to continue.");
      return;
    }

    setResult(null);
    setError("");
    await loadQuestion(moduleKey, difficulty);
  };

  const onSubmit = async (answer: string) => {
    if (!question) {
      return;
    }

    if (freePracticeLocked) {
      setError("You have used all 12 free questions. Subscribe or log in with your activation code to continue.");
      return;
    }

    setError("");

    try {
      const response = await handleSubmit({
        session_id: sessionId,
        module: question.module,
        difficulty: question.difficulty,
        question_id: question.question_id,
        validation_token: question.validation_token,
        user_answer: answer,
      });

      if (response.session_summary) {
        setSessionSummary(response.session_summary);
      }

      if (!isAuthenticated) {
        setFreeAttemptsUsed((previous) => {
          const next = previous + 1;
          writeStoredFreeAttempts(next);
          return next;
        });
      }
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Unable to submit answer");
    }
  };

  const onRestartSession = async () => {
    if (freePracticeLocked) {
      setError("You have used all 12 free questions. Subscribe or log in with your activation code to continue.");
      return;
    }

    setResult(null);
    setSessionSummary(undefined);
    setError("");
    await startSession();
    await loadQuestion(moduleKey, difficulty);
  };

  return (
    <div className="grid gap-6 pt-8 lg:grid-cols-[1.5fr_0.9fr]">
      <section className="space-y-6">
        <ModuleTabs currentModule={moduleKey} />

        <div className="grid gap-4 sm:grid-cols-[220px_1fr]">
          <DifficultySelector difficulty={difficulty} onChange={setDifficulty} />

          <div className="flex items-end gap-3">
            <Button
              onClick={() => void onNewQuestion()}
              disabled={isLoading || isCreating || freePracticeLocked}
            >
              {isLoading ? "Loading..." : "New question"}
            </Button>

            <Button
              variant="secondary"
              onClick={() => void onRestartSession()}
              disabled={isCreating || freePracticeLocked}
            >
              Restart session
            </Button>
          </div>
        </div>

        {isCreating ? <Loader /> : null}

        {error ? (
          <p className="rounded-2xl border border-rose-800 bg-rose-950/40 px-4 py-3 text-sm text-rose-300">
            {error}
          </p>
        ) : null}

        {!isAuthenticated ? (
          <div className="rounded-3xl border border-cyan-900 bg-cyan-950/30 p-5">
            <div className="flex items-center justify-between gap-4">
              <div>
                <h3 className="text-base font-semibold text-white">Free practice</h3>
                <p className="mt-1 text-sm text-slate-300">
                  You can answer up to {FREE_PRACTICE_LIMIT} free questions before payment is required.
                </p>
              </div>

              <div className="rounded-2xl bg-slate-950 px-4 py-3 text-right">
                <div className="text-xs uppercase tracking-wide text-slate-400">
                  Remaining
                </div>
                <div className="text-2xl font-bold text-cyan-300">
                  {freeQuestionsRemaining}
                </div>
              </div>
            </div>
          </div>
        ) : null}

        <QuestionCard question={question} />

        {isLoading ? <Loader /> : null}

        <SubmitAnswerForm
          question={question}
          isSubmitting={isSubmitting || freePracticeLocked}
          onSubmit={onSubmit}
        />

        <QuestionExplanation result={result} />

        {freePracticeLocked ? (
          <div className="rounded-3xl border border-amber-500/30 bg-amber-500/10 p-6">
            <h3 className="text-xl font-semibold text-white">
              Your 12 free questions are used up
            </h3>
            <p className="mt-2 text-sm text-slate-200">
              To continue practicing, subscribe or log in with your activation code.
            </p>

            <div className="mt-4 flex flex-col gap-3 sm:flex-row">
              <Link
                to="/pricing"
                className="inline-flex items-center justify-center rounded-2xl bg-amber-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-amber-300"
              >
                View pricing
              </Link>

              <Link
                to="/login"
                className="inline-flex items-center justify-center rounded-2xl border border-slate-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
              >
                Log in with code
              </Link>
            </div>
          </div>
        ) : null}
      </section>

      <aside className="space-y-6">
        <ScorePanel summary={sessionSummary} />

        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-panel">
          <h3 className="mb-3 text-lg font-semibold text-white">How to answer</h3>

          <ul className="space-y-3 text-sm text-slate-300">
            <li>
              • Use plain text like <span className="font-mono text-cyan-300">-7</span> or{" "}
              <span className="font-mono text-cyan-300">14</span> for number answers.
            </li>
            <li>
              • Use <span className="font-mono text-cyan-300">x^2</span> or{" "}
              <span className="font-mono text-cyan-300">(x+3)(x-3)</span> for algebra.
            </li>
            <li>• For multiple choice, click an option and submit.</li>
          </ul>
        </div>
      </aside>
    </div>
  );
}