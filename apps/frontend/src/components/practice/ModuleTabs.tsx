import { useNavigate } from "react-router-dom";
import type { ModuleKey } from "../../types/question";

const modules: Array<{ key: ModuleKey; label: string }> = [
  { key: "integer-operations", label: "Integer operations" },
  { key: "algebra-expressions", label: "Algebra expressions" },
  { key: "algebra-formulas", label: "Algebra formulas" }
];

interface ModuleTabsProps {
  currentModule: ModuleKey;
}

export function ModuleTabs({ currentModule }: ModuleTabsProps) {
  const navigate = useNavigate();

  return (
    <div className="grid gap-2 sm:grid-cols-3">
      {modules.map((module) => (
        <button
          key={module.key}
          onClick={() => navigate(`/practice/${module.key}`)}
          className={[
            "rounded-2xl border px-4 py-3 text-left text-sm font-medium transition",
            module.key === currentModule
              ? "border-cyan-500 bg-cyan-500/10 text-cyan-300"
              : "border-slate-800 bg-slate-900 text-slate-300 hover:border-slate-700 hover:text-white"
          ].join(" ")}
        >
          {module.label}
        </button>
      ))}
    </div>
  );
}
