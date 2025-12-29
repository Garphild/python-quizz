export interface AttemptLocal {
  attemptId: string;
  quizId: number;
  startedAt: number;
  finishedAt?: number;
  questionOrder: number[];
  answers: AttemptAnswerLocal[];
  score?: number;
  total?: number;
}

export interface AttemptAnswerLocal {
  questionId: number;
  selectedOptionId: number;
  isCorrect: boolean;
  correctOptionId?: number;
  explanation?: string;
}

export interface QuizStatsLocal {
  quizId: number;
  attemptsCount: number;
  bestScore: number;
  lastScore: number;
  lastAttemptAt: number;
}
