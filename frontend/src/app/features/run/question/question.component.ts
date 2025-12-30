import { Component, inject, ChangeDetectionStrategy, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { QuizService } from '../../../core/services/quiz.service';
import { AttemptRepository } from '../../../persistence/attempt.repository';
import { AppStateRepository } from '../../../persistence/app-state.repository';
import { AttemptLocal } from '../../../core/models/attempt.models';

@Component({
  selector: 'app-question',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatRadioModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatIconModule,
    ReactiveFormsModule,
    TranslateModule
  ],
  template: `
    <div class="question-page">
      @if (isLoading()) {
        <div class="loading-container">
          <mat-spinner diameter="48"></mat-spinner>
          <p>{{ 'COMMON.LOADING' | translate }}</p>
        </div>
      } @else if (attempt() && question() && answers()) {
        <div class="question-container slide-up">
          <!-- Progress Header -->
          <div class="progress-header">
            <div class="progress-info">
              <span class="progress-label">{{ 'RUN.QUESTION' | translate }}</span>
              <span class="progress-count">{{ currentIndex() + 1 }} {{ 'RUN.OF' | translate }} {{ attempt()!.questionOrder.length }}</span>
            </div>
            <mat-progress-bar 
              mode="determinate" 
              [value]="progressPercent()">
            </mat-progress-bar>
          </div>

          <!-- Question Card -->
          <div class="question-card">
            <div class="question-number">
              <mat-icon>help_outline</mat-icon>
              {{ 'RUN.QUESTION' | translate }} {{ currentIndex() + 1 }}
            </div>
            <h2 class="question-text">{{ question()!.text }}</h2>
            
            <form [formGroup]="form" class="answers-form">
              <mat-radio-group formControlName="answer" aria-label="Select an answer">
                @for (answer of answers(); track answer.id; let i = $index) {
                  <label class="answer-option" [class.selected]="isAnswerSelected(answer.id)">
                    <mat-radio-button [value]="answer.id">
                      <span class="answer-letter">{{ getAnswerLetter(i) }}</span>
                      <span class="answer-text">{{ answer.text }}</span>
                    </mat-radio-button>
                  </label>
                }
              </mat-radio-group>
            </form>

            <button 
              mat-raised-button 
              color="primary" 
              class="submit-btn"
              (click)="onSubmit()"
              [disabled]="!form.get('answer')?.value || isSubmitting()">
              @if (isSubmitting()) {
                <mat-spinner diameter="20"></mat-spinner>
              } @else {
                <ng-container>
                  <mat-icon>check_circle</mat-icon>
                  {{ 'RUN.SUBMIT_ANSWER' | translate }}
                </ng-container>
              }
            </button>
          </div>
        </div>
      }
    </div>
  `,
  styles: [`
    .question-page {
      min-height: calc(100vh - 64px);
      padding: var(--spacing-6);
      background: linear-gradient(135deg, var(--color-background) 0%, #e3f2fd 100%);
    }

    .loading-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 50vh;
    }

    .loading-container p {
      margin-top: var(--spacing-4);
      color: var(--color-text-secondary);
    }

    .question-container {
      max-width: 700px;
      margin: 0 auto;
    }

    .progress-header {
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      padding: var(--spacing-4) var(--spacing-6);
      margin-bottom: var(--spacing-6);
      box-shadow: var(--shadow-sm);
    }

    .progress-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: var(--spacing-3);
    }

    .progress-label {
      font-size: var(--font-size-body2);
      color: var(--color-text-secondary);
    }

    .progress-count {
      font-size: var(--font-size-body1);
      font-weight: var(--font-weight-medium);
      color: var(--color-primary);
    }

    mat-progress-bar {
      height: 8px !important;
      border-radius: 4px;
    }

    .question-card {
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      padding: var(--spacing-8);
      box-shadow: var(--shadow-lg);
    }

    .question-number {
      display: flex;
      align-items: center;
      gap: var(--spacing-2);
      font-size: var(--font-size-body2);
      color: var(--color-primary);
      font-weight: var(--font-weight-medium);
      margin-bottom: var(--spacing-4);
    }

    .question-number mat-icon {
      font-size: 20px;
      width: 20px;
      height: 20px;
    }

    .question-text {
      font-size: var(--font-size-h3);
      font-weight: var(--font-weight-medium);
      color: var(--color-text-primary);
      margin-bottom: var(--spacing-8);
      line-height: 1.5;
    }

    .answers-form {
      margin-bottom: var(--spacing-6);
    }

    mat-radio-group {
      display: flex;
      flex-direction: column;
      gap: var(--spacing-3);
    }

    .answer-option {
      display: block;
      border: 2px solid var(--color-divider);
      border-radius: var(--radius-md);
      padding: var(--spacing-4);
      cursor: pointer;
      transition: all var(--transition-fast);
    }

    .answer-option:hover {
      border-color: var(--color-primary-light);
      background: rgba(25, 118, 210, 0.04);
    }

    .answer-option.selected {
      border-color: var(--color-primary);
      background: rgba(25, 118, 210, 0.08);
    }

    .answer-option mat-radio-button {
      width: 100%;
    }

    .answer-letter {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 28px;
      height: 28px;
      background: var(--color-primary);
      color: white;
      border-radius: 50%;
      font-size: var(--font-size-body2);
      font-weight: var(--font-weight-bold);
      margin-right: var(--spacing-3);
    }

    .answer-text {
      font-size: var(--font-size-body1);
    }

    .submit-btn {
      width: 100%;
      padding: var(--spacing-4) !important;
      font-size: var(--font-size-body1) !important;
      border-radius: var(--radius-md) !important;
    }

    .submit-btn mat-icon {
      margin-right: var(--spacing-2);
    }

    @media (max-width: 600px) {
      .question-card {
        padding: var(--spacing-5);
      }

      .question-text {
        font-size: var(--font-size-h4);
      }
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class QuestionComponent implements OnInit {
  private quizService = inject(QuizService);
  private attemptRepo = inject(AttemptRepository);
  private appStateRepo = inject(AppStateRepository);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private fb = inject(FormBuilder);

  isLoading = signal(false);
  isSubmitting = signal(false);
  attempt = signal<AttemptLocal | null>(null);
  question = signal<{ id: number; text: string } | null>(null);
  answers = signal<{ id: number; text: string }[]>([]);
  currentIndex = signal(0);
  quizId = 0;
  form = this.fb.group({ answer: [''] });

  progressPercent(): number {
    const att = this.attempt();
    if (!att) return 0;
    return ((this.currentIndex() + 1) / att.questionOrder.length) * 100;
  }

  getAnswerLetter(index: number): string {
    return String.fromCharCode(65 + index);
  }

  isAnswerSelected(answerId: number): boolean {
    const value = this.form.get('answer')?.value;
    return value !== null && value !== undefined && Number(value) === answerId;
  }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    const index = this.route.snapshot.paramMap.get('index');
    this.quizId = id ? Number(id) : 0;
    this.currentIndex.set(index ? Number(index) : 0);
    this.loadQuestion();
  }

  async loadQuestion(): Promise<void> {
    this.isLoading.set(true);
    try {
      const attemptId = await this.appStateRepo.getActiveAttempt(this.quizId);
      if (!attemptId) throw new Error('No active attempt');

      const attempt = await this.attemptRepo.getAttempt(attemptId);
      if (!attempt) throw new Error('Attempt not found');

      this.attempt.set(attempt);
      const questionId = attempt.questionOrder[this.currentIndex()];
      const question = await this.quizService.getQuestion(this.quizId, questionId).toPromise();
      if (!question) throw new Error('Question not found');

      this.question.set(question);
      const answers = await this.quizService.getAnswers(this.quizId).toPromise();
      this.answers.set(answers || []);
      this.isLoading.set(false);
    } catch (error) {
      this.isLoading.set(false);
    }
  }

  async onSubmit(): Promise<void> {
    if (!this.form.get('answer')?.value) return;

    this.isSubmitting.set(true);
    try {
      const answerId = Number(this.form.get('answer')?.value);
      const questionId = this.question()!.id;
      
      await this.quizService.validateAnswer(this.quizId, questionId, answerId).toPromise();
      
      const attempt = this.attempt()!;
      const attemptId = attempt.attemptId;
      await this.attemptRepo.appendAnswer(attemptId, {
        questionId,
        selectedOptionId: answerId,
        isCorrect: true
      });

      this.router.navigate(['/app/quizzes', this.quizId, 'run', 'feedback']);
    } catch (error) {
      this.isSubmitting.set(false);
    }
  }
}
