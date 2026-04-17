import { Link } from "react-router-dom";

export function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div>
            <p className="mb-4 inline-flex rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-sm font-medium text-cyan-300">
              Practice smarter
            </p>

            <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
              Learn integers, algebra expressions, and formulas with instant feedback
            </h1>

            <p className="mt-6 max-w-2xl text-base leading-7 text-slate-300 sm:text-lg">
              Build confidence with generated practice questions, difficulty levels,
              and short explanations after every answer.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Link
                to="/practice"
                className="inline-flex items-center justify-center rounded-2xl bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300"
              >
                Browse modules
              </Link>

              <Link
                to="/pricing"
                className="inline-flex items-center justify-center rounded-2xl border border-slate-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
              >
                View pricing
              </Link>

              <Link
                to="/login"
                className="inline-flex items-center justify-center rounded-2xl border border-emerald-500/40 bg-emerald-500/10 px-5 py-3 text-sm font-semibold text-emerald-300 transition hover:bg-emerald-500/20"
              >
                Log in with code
              </Link>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl">
            <h2 className="text-xl font-semibold">What students can practice</h2>

            <div className="mt-6 grid gap-4">
              <div className="rounded-2xl border border-slate-800 bg-slate-950/50 p-4">
                <h3 className="font-medium text-cyan-300">Integer operations</h3>
                <p className="mt-2 text-sm text-slate-300">
                  Positive and negative numbers, mixed signs, and arithmetic fluency.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-800 bg-slate-950/50 p-4">
                <h3 className="font-medium text-cyan-300">Algebra expressions</h3>
                <p className="mt-2 text-sm text-slate-300">
                  Simplify, expand, collect like terms, and evaluate expressions.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-800 bg-slate-950/50 p-4">
                <h3 className="font-medium text-cyan-300">Algebra formulas</h3>
                <p className="mt-2 text-sm text-slate-300">
                  Identify formulas and apply them to solve structured questions.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}