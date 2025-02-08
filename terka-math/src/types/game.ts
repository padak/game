export interface Cell {
  value: number | null;
  isOperator: boolean;
  operator?: '+' | '-' | '*' | '=' | null;
  isFixed: boolean;
  isResult: boolean;
  isCorrect?: boolean;
  isIncorrect?: boolean;
  isEmpty?: boolean;
  inEquation?: boolean;
} 