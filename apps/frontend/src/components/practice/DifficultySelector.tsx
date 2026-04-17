import { Select } from "../common/Select";
import type { Difficulty } from "../../types/question";

interface DifficultySelectorProps {
  difficulty: Difficulty;
  onChange: (nextValue: Difficulty) => void;
}

export function DifficultySelector({ difficulty, onChange }: DifficultySelectorProps) {
  return (
    <div>
      <label className="mb-2 block text-sm font-medium text-slate-300">Difficulty</label>
      <Select value={difficulty} onChange={(event) => onChange(event.target.value as Difficulty)}>
        <option value="easy">Easy</option>
        <option value="medium">Medium</option>
        <option value="hard">Hard</option>
      </Select>
    </div>
  );
}
