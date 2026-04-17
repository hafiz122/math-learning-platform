import { Link } from "react-router-dom";

const whatsappNumber = "60123456789"; // replace with your real number
const whatsappMessage = encodeURIComponent(
  "Hi, I want to subscribe to the Math Learning Platform for RM30/month."
);

export function PricingPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <section className="mx-auto max-w-5xl px-6 py-16">
        <div className="mx-auto max-w-2xl text-center">
          <p className="mb-3 inline-flex rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-sm font-medium text-emerald-300">
            Simple monthly plan
          </p>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Pricing
          </h1>
          <p className="mt-4 text-base text-slate-300 sm:text-lg">
            Get full access to math practice modules, guided explanations, and
            continuous practice for a simple monthly fee.
          </p>
        </div>

        <div className="mx-auto mt-12 max-w-xl rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl">
          <div className="text-center">
            <h2 className="text-2xl font-semibold">Premium Plan</h2>
            <div className="mt-4">
              <span className="text-5xl font-bold">RM30</span>
              <span className="ml-2 text-slate-400">/ month</span>
            </div>
            <p className="mt-4 text-sm text-slate-400">
              Manual activation via WhatsApp after payment confirmation.
            </p>
          </div>

          <ul className="mt-8 space-y-4 text-sm text-slate-200">
            <li className="rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3">
              Unlimited practice across all 3 learning modules
            </li>
            <li className="rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3">
              Easy, medium, and hard difficulty levels
            </li>
            <li className="rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3">
              Instant answer checking and explanations
            </li>
            <li className="rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3">
              Future premium features and progress tracking
            </li>
          </ul>

          <div className="mt-8 flex flex-col gap-3">
            <a
              href={`https://wa.me/${whatsappNumber}?text=${whatsappMessage}`}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center rounded-2xl bg-emerald-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-emerald-400"
            >
              Contact to Subscribe
            </a>

            <Link
              to="/practice"
              className="inline-flex items-center justify-center rounded-2xl border border-slate-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
            >
              Continue Free Practice
            </Link>
          </div>

          <div className="mt-8 rounded-2xl border border-amber-400/20 bg-amber-400/10 p-4 text-sm text-amber-100">
            <p className="font-semibold">How it works</p>
            <p className="mt-2">
              Click the subscribe button, message us on WhatsApp, make payment,
              and send your payment proof. Your access will be activated
              manually.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}