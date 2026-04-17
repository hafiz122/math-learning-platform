export type ModuleKey = "integer-operations" | "algebra-expressions" | "algebra-formulas";
export type Difficulty = "easy" | "medium" | "hard";
export type InputType = "text" | "multiple_choice";

export interface ChoiceOption {
  key: string;
  label: string;
}

export interface Question {
  question_id: string;
  module: ModuleKey;
  difficulty: Difficulty;
  prompt: string;
  input_type: InputType;
  question_kind: string;
  placeholder?: string;
  choices?: ChoiceOption[];
  validation_token: string;
}
