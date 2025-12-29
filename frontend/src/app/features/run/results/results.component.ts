import { Component, inject, ChangeDetectionStrategy, signal, OnInit, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { TranslateModule } from '@ngx-translate/core';
import { AttemptRepository } from '../../../persistence/attempt.repository';
import { QuizStatsRepository } from '../../../persistence/quiz-stats.repository';
import { AppStateRepository } from '../../../persistence/app-state.repository';
import { AttemptLocal } from '../../../core/models/attempt.models';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatIconModule,
    TranslateModule
  ],
  template: `
    <div class="results-page">
      @if (isLoading()) {
        <div class="loading-container">
          <mat-spinner diameter="48"></mat-spinner>
          <p>Calculating results...</p>
        </div>
      } @else if (attempt()) {
        <div class="results-container slide-up">
          <div class="results-icon" [class.success]="percentage() >= 70" [class.warning]="percentage() >= 40 && percentage() < 70" [class.error]="percentage() < 40">
            <mat-icon>{{ getResultIcon() }}</mat-icon>
          </div>

          <h1>{{ getResultTitle() }}</h1>
          <p class="result-message">{{ getResultMessage() }}</p>

          <div class="score-card">
            <div class="score-display">
              <span class="score-value">{{ attempt()!.score }}</span>
              <span class="score-separator">/</span>
              <span class="score-total">{{ attempt()!.total }}</span>
            </div>
            <div class="percentage-display">
              <span class="percentage-value">{{ percentage() }}%</span>
              <span class="percentage-label">correct</span>
            </div>
            <mat-progress-bar 
              mode="determinate" 
              [value]="percentage()"
              [color]="getProgressColor()">
            </mat-progress-bar>
          </div>

          <div class="action-buttons">
            <button mat-raised-button color="primary" (click)="onRetry()" class="action-btn">
              <mat-icon>replay</mat-icon>
              Try Again
            </button>
            <button mat-stroked-button (click)="onBackToList()" class="action-btn">
              <mat-icon>list</mat-icon>
              Back to Quizzes
            </button>
          </div>
        </div>
      }
    </div>
  `,
  styles: [`
    .results-page {
      min-height: calc(100vh - 64px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: var(--spacing-8);
      background: linear-gradient(135deg, var(--color-background) 0%, #e8f5e9 100%);
    }

    .loading-container {
      text-align: center;
    }

    .loading-container p {
      margin-top: var(--spacing-4);
      color: var(--color-text-secondary);
    }

    .results-container {
      text-align: center;
      max-width: 480px;
      width: 100%;
    }

    .results-icon {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-bottom: var(--spacing-6);
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    }

    .results-icon.success {
      background: linear-gradient(135deg, var(--color-success) 0%, #2e7d32 100%);
    }

    .results-icon.warning {
      background: linear-gradient(135deg, var(--color-warning) 0%, #f57c00 100%);
    }

    .results-icon.error {
      background: linear-gradient(135deg, var(--color-error) 0%, #c62828 100%);
    }

    .results-icon mat-icon {
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

    .score-card {
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      padding: var(--spacing-8);
      box-shadow: var(--shadow-lg);
      margin-bottom: var(--spacing-8);
    }

    .score-display {
      display: flex;
      align-items: baseline;
      justify-content: center;
      gap: var(--spacing-2);
      margin-bottom: var(--spacing-4);
    }

    .score-value {
      font-size: 64px;
      font-weight: var(--font-weight-bold);
      color: var(--color-primary);
    }

    .score-separator {
      font-size: 32px;
      color: var(--color-text-secondary);
    }

    .score-total {
      font-size: 32px;
      color: var(--color-text-secondary);
    }

    .percentage-display {
      display: flex;
      align-items: baseline;
      justify-content: center;
      gap: var(--spacing-2);
      margin-bottom: var(--spacing-6);
    }

    .percentage-value {
      font-size: var(--font-size-h2);
      font-weight: var(--font-weight-medium);
      color: var(--color-text-primary);
    }

    .percentage-label {
      font-size: var(--font-size-body2);
      color: var(--color-text-secondary);
    }

    mat-progress-bar {
      height: 8px !important;
      border-radius: 4px;
    }

    .action-buttons {
      display: flex;
      gap: var(--spacing-4);
    }

    .action-btn {
      flex: 1;
      padding: var(--spacing-4) var(--spacing-6) !important;
      border-radius: var(--radius-md) !important;
    }

    .action-btn mat-icon {
      margin-right: var(--spacing-2);
    }

    @media (max-width: 600px) {
      .action-buttons {
        flex-direction: column;
      }

      .score-value {
        font-size: 48px;
      }
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ResultsComponent implements OnInit {
  private attemptRepo = inject(AttemptRepository);
  private statsRepo = inject(QuizStatsRepository);
  private appStateRepo = inject(AppStateRepository);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  isLoading = signal(false);
  attempt = signal<AttemptLocal | null>(null);
  quizId = 0;

  percentage = signal(0);

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.quizId = id ? Number(id) : 0;
    this.loadResults();
  }

  async loadResults(): Promise<void> {
    this.isLoading.set(true);
    try {
      const attemptId = await this.appStateRepo.getActiveAttempt(this.quizId);
      if (!attemptId) throw new Error('No active attempt');

      const attempt = await this.attemptRepo.getAttempt(attemptId);
      if (!attempt) throw new Error('Attempt not found');

      this.attempt.set(attempt);
      const pct = attempt.total ? Math.round((attempt.score! / attempt.total) * 100) : 0;
      this.percentage.set(pct);

      await this.statsRepo.updateAfterAttempt(this.quizId, attempt.score || 0);
      await this.appStateRepo.clearActiveAttempt(this.quizId);
      this.isLoading.set(false);
    } catch (error) {
      this.isLoading.set(false);
    }
  }

  getResultIcon(): string {
    const pct = this.percentage();
    if (pct >= 70) return 'emoji_events';
    if (pct >= 40) return 'thumb_up';
    return 'sentiment_dissatisfied';
  }

  getResultTitle(): string {
    const pct = this.percentage();
    if (pct >= 70) return 'Excellent!';
    if (pct >= 40) return 'Good Job!';
    return 'Keep Learning!';
  }

  getResultMessage(): string {
    const pct = this.percentage();
    if (pct >= 70) return 'You have mastered this quiz!';
    if (pct >= 40) return 'You are making progress. Keep it up!';
    return 'Don\'t give up! Practice makes perfect.';
  }

  getProgressColor(): string {
    const pct = this.percentage();
    if (pct >= 70) return 'primary';
    if (pct >= 40) return 'accent';
    return 'warn';
  }

  onRetry(): void {
    this.router.navigate(['/app/quizzes', this.quizId, 'run']);
  }

  onBackToList(): void {
    this.router.navigate(['/app/quizzes']);
  }
}
