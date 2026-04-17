import { Card } from "../common/Card";
import type { SessionSummary } from "../../types/api";

interface ScorePanelProps {
  summary?: SessionSummary;
}

export function ScorePanel({ summary }: ScorePanelProps) {
  return (
    <Card>
      <h3 className="mb-4 text-lg font-semibold text-white">Session score</h3>

      {!summary ? (
        <p className="text-sm text-slate-400">No answers submitted yet.</p>
      ) : (
        <div className="grid grid-cols-3 gap-3">
          <Metric label="Attempts" value={summary.attempts} />
          <Metric label="Correct" value={summary.correct_attempts} />
          <Metric label="Accuracy" value={`${summary.accuracy}%`} />
        </div>
      )}
    </Card>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
      <p className="text-xs uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-bold text-white">{value}</p>
    </div>
  );
}
