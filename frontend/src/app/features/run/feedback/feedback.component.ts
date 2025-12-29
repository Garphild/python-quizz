import { Component, inject, ChangeDetectionStrategy, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { TranslateModule } from '@ngx-translate/core';
import { AttemptRepository } from '../../../persistence/attempt.repository';
import { AppStateRepository } from '../../../persistence/app-state.repository';

@Component({
  selector: 'app-feedback',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatIconModule, TranslateModule],
  template: `
    <div class="feedback-page">
      <div class="feedback-container slide-up">
        <!-- Result Icon -->
        <div class="result-icon" [class.correct]="isCorrect()" [class.incorrect]="!isCorrect()">
          <mat-icon>{{ isCorrect() ? 'check_circle' : 'cancel' }}</mat-icon>
        </div>

        <!-- Result Title -->
        <h1>{{ isCorrect() ? 'Correct!' : 'Incorrect' }}</h1>
        <p class="result-message">
          {{ isCorrect() ? 'Great job! You got it right.' : 'Don\'t worry, keep learning!' }}
        </p>

        <!-- Feedback Card -->
        <div class="feedback-card">
          <div class="answer-section">
            <div class="answer-label">Your answer</div>
            <div class="answer-text" [class.correct]="isCorrect()" [class.incorrect]="!isCorrect()">
              <mat-icon>{{ isCorrect() ? 'check' : 'close' }}</mat-icon>
              {{ selectedAnswerText() }}
            </div>
          </div>

          @if (!isCorrect() && correctAnswerText()) {
            <div class="answer-section correct-section">
              <div class="answer-label">Correct answer</div>
              <div class="answer-text correct">
                <mat-icon>check</mat-icon>
                {{ correctAnswerText() }}
              </div>
            </div>
          }
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          @if (hasMoreQuestions()) {
            <button mat-raised-button color="primary" class="action-btn" (click)="onNext()">
              <mat-icon>arrow_forward</mat-icon>
              Next Question
            </button>
          } @else {
            <button mat-raised-button color="primary" class="action-btn" (click)="onFinish()">
              <mat-icon>emoji_events</mat-icon>
              See Results
            </button>
          }
        </div>
      </div>
    </div>
  `,
  styles: [`
    .feedback-page {
      min-height: calc(100vh - 64px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: var(--spacing-8);
      background: linear-gradient(135deg, var(--color-background) 0%, #e8f5e9 100%);
    }

    .feedback-container {
      text-align: center;
      max-width: 500px;
      width: 100%;
    }

    .result-icon {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-bottom: var(--spacing-6);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    }

    .result-icon.correct {
      background: linear-gradient(135deg, var(--color-success) 0%, #2e7d32 100%);
    }

    .result-icon.incorrect {
      background: linear-gradient(135deg, var(--color-error) 0%, #c62828 100%);
    }

    .result-icon mat-icon {
      font-size: 48px;
      width: 48px;
      height: 48px;
      color: white;
    }

    h1 {
      font-size: var(--font-size-h1);
      font-weight: var(--font-weight-bold);
      margin-bottom: var(--spacing-2);
      color: var(--color-text-primary);
    }

    .result-message {
      font-size: var(--font-size-body1);
      color: var(--color-text-secondary);
      margin-bottom: var(--spacing-8);
    }

    .feedback-card {
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      padding: var(--spacing-6);
      box-shadow: var(--shadow-lg);
      margin-bottom: var(--spacing-8);
      text-align: left;
    }

    .answer-section {
      margin-bottom: var(--spacing-4);
    }

    .answer-section:last-child {
      margin-bottom: 0;
    }

    .correct-section {
      padding-top: var(--spacing-4);
      border-top: 1px solid var(--color-divider);
    }

    .answer-label {
      font-size: var(--font-size-caption);
      color: var(--color-text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: var(--spacing-2);
    }

    .answer-text {
      display: flex;
      align-items: center;
      gap: var(--spacing-2);
      padding: var(--spacing-3) var(--spacing-4);
      border-radius: var(--radius-md);
      font-weight: var(--font-weight-medium);
    }

    .answer-text.correct {
      background: rgba(76, 175, 80, 0.1);
      color: var(--color-success);
    }

    .answer-text.incorrect {
      background: rgba(244, 67, 54, 0.1);
      color: var(--color-error);
    }

    .answer-text mat-icon {
      font-size: 20px;
      width: 20px;
      height: 20px;
    }

    .action-buttons {
      display: flex;
      gap: var(--spacing-4);
    }

    .action-btn {
      flex: 1;
      padding: var(--spacing-4) var(--spacing-6) !important;
      border-radius: var(--radius-md) !important;
      font-size: var(--font-size-body1) !important;
    }

    .action-btn mat-icon {
      margin-right: var(--spacing-2);
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeedbackComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private attemptRepo = inject(AttemptRepository);
  private appStateRepo = inject(AppStateRepository);

  quizId = 0;
  currentIndex = 0;
  totalQuestions = signal(0);
  isCorrect = signal(true);
  selectedAnswerText = signal('');
  correctAnswerText = signal('');

  ngOnInit(): void {
    this.quizId = Number(this.route.snapshot.paramMap.get('id'));
    this.currentIndex = Number(this.route.snapshot.paramMap.get('index')) || 0;
    this.loadFeedbackData();
  }

  async loadFeedbackData(): Promise<void> {
    try {
      const attemptId = await this.appStateRepo.getActiveAttempt(this.quizId);
      if (attemptId) {
        const attempt = await this.attemptRepo.getAttempt(attemptId);
        if (attempt) {
          this.totalQuestions.set(attempt.questionOrder.length);
          const lastAnswer = attempt.answers[attempt.answers.length - 1];
          if (lastAnswer) {
            this.isCorrect.set(lastAnswer.isCorrect);
          }
        }
      }
    } catch {
      // Use defaults
    }
  }

  hasMoreQuestions(): boolean {
    return this.currentIndex < this.totalQuestions() - 1;
  }

  onNext(): void {
    this.router.navigate(['/app/quizzes', this.quizId, 'run', 'q', this.currentIndex + 1]);
  }

  onFinish(): void {
    this.router.navigate(['/app/quizzes', this.quizId, 'run', 'results']);
  }
}
