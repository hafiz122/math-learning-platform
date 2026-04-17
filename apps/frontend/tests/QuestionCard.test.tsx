import { render, screen } from "@testing-library/react";
import { QuestionCard } from "../src/components/practice/QuestionCard";

describe("QuestionCard", () => {
  it("renders prompt and choices", () => {
    render(
      <QuestionCard
        question={{
          question_id: "q1",
          module: "algebra-formulas",
          difficulty: "easy",
          prompt: "Which formula matches (a+b)^2?",
          input_type: "multiple_choice",
          question_kind: "identify_formula",
          validation_token: "token",
          choices: [
            { key: "A", label: "a^2 + 2ab + b^2" },
            { key: "B", label: "a^2 - b^2" }
          ]
        }}
      />
    );

    expect(screen.getByText(/Which formula matches/i)).toBeInTheDocument();
    expect(screen.getByText(/a\^2 \+ 2ab \+ b\^2/i)).toBeInTheDocument();
  });
});
