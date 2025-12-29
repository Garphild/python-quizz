export interface QuizzDto {
  id: number;
  name: string;
  description: string;
  url: string;
  questions_count: number;
  created_at?: string;
  updated_at?: string;
  deleted_at?: string;
}

export interface CreateQuizzDto {
  url: string;
}

export interface UpdateQuizzDto {
  name?: string;
  description?: string;
}

export interface QuestionDto {
  id: number;
  text: string;
  quizz_id: number;
  created_at: string;
  updated_at: string;
  deleted_at?: string;
}

export interface CreateQuestionDto {
  text: string;
}

export interface UpdateQuestionDto {
  text: string;
}

export interface QuestionListDto {
  questions: QuestionDto[];
}

export interface AnswerDto {
  id: number;
  text: string;
  is_correct: boolean;
  question_id: number;
  description: string;
  valid_description?: string;
}

export interface CreateAnswerDto {
  text: string;
  is_correct: boolean;
  description: string;
  valid_description?: string;
}

export interface UpdateAnswerDto {
  text: string;
  is_correct: boolean;
  description: string;
  valid_description?: string;
}

export interface ValidateAnswerDto {
  is_correct: boolean;
  description: string;
  valid_description?: string;
}
