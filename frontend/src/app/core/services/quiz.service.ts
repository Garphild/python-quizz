import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  QuizzDto,
  CreateQuizzDto,
  UpdateQuizzDto,
  QuestionDto,
  CreateQuestionDto,
  UpdateQuestionDto,
  AnswerDto,
  CreateAnswerDto,
  UpdateAnswerDto,
  ValidateAnswerDto
} from '../models/quiz.models';

@Injectable({ providedIn: 'root' })
export class QuizService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiBasePath}/quizz`;

  // Quizzes
  getQuizzes(): Observable<QuizzDto[]> {
    return this.http.get<QuizzDto[]>(this.apiUrl);
  }

  getQuiz(id: number): Observable<QuizzDto> {
    return this.http.get<QuizzDto>(`${this.apiUrl}/${id}`);
  }

  createQuiz(data: CreateQuizzDto): Observable<QuizzDto> {
    return this.http.post<QuizzDto>(this.apiUrl, data);
  }

  updateQuiz(id: number, data: UpdateQuizzDto): Observable<QuizzDto> {
    return this.http.put<QuizzDto>(`${this.apiUrl}/${id}`, data);
  }

  deleteQuiz(id: number): Observable<boolean> {
    return this.http.delete<boolean>(`${this.apiUrl}/${id}`);
  }

  // Questions
  getQuestions(quizId: number): Observable<QuestionDto[]> {
    return this.http.get<QuestionDto[]>(`${this.apiUrl}/${quizId}/questions`);
  }

  getQuestion(quizId: number, questionId: number): Observable<QuestionDto> {
    return this.http.get<QuestionDto>(`${this.apiUrl}/${quizId}/questions/${questionId}`);
  }

  createQuestion(quizId: number, data: CreateQuestionDto): Observable<QuestionDto> {
    return this.http.post<QuestionDto>(`${this.apiUrl}/${quizId}/questions`, data);
  }

  updateQuestion(quizId: number, questionId: number, data: UpdateQuestionDto): Observable<QuestionDto> {
    return this.http.put<QuestionDto>(`${this.apiUrl}/${quizId}/questions/${questionId}`, data);
  }

  deleteQuestion(quizId: number, questionId: number): Observable<boolean> {
    return this.http.delete<boolean>(`${this.apiUrl}/${quizId}/questions/${questionId}`);
  }

  // Answers
  getAnswers(quizId: number): Observable<AnswerDto[]> {
    return this.http.get<AnswerDto[]>(`${this.apiUrl}/${quizId}/answers`);
  }

  getAnswer(quizId: number, answerId: number): Observable<AnswerDto> {
    return this.http.get<AnswerDto>(`${this.apiUrl}/${quizId}/answers/${answerId}`);
  }

  createAnswer(quizId: number, data: CreateAnswerDto): Observable<AnswerDto> {
    return this.http.post<AnswerDto>(`${this.apiUrl}/${quizId}/answers`, data);
  }

  updateAnswer(quizId: number, answerId: number, data: UpdateAnswerDto): Observable<AnswerDto> {
    return this.http.put<AnswerDto>(`${this.apiUrl}/${quizId}/answers/${answerId}`, data);
  }

  deleteAnswer(quizId: number, answerId: number): Observable<boolean> {
    return this.http.delete<boolean>(`${this.apiUrl}/${quizId}/answers/${answerId}`);
  }

  validateAnswer(quizId: number, questionId: number, answerId: number): Observable<ValidateAnswerDto> {
    return this.http.get<ValidateAnswerDto>(`${this.apiUrl}/${quizId}/answers/validate/${questionId}/${answerId}`);
  }
}
