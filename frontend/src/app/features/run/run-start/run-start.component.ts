import { Component, inject, ChangeDetectionStrategy, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { TranslateModule } from '@ngx-translate/core';
import { QuizService } from '../../../core/services/quiz.service';
import { AttemptRepository } from '../../../persistence/attempt.repository';
import { AppStateRepository } from '../../../persistence/app-state.repository';

@Component({
  selector: 'app-run-start',
  standalone: true,
  imports: [CommonModule, RouterModule, MatButtonModule, MatProgressSpinnerModule, MatIconModule, TranslateModule],
  template: `
    <div class="run-start-page">
      @if (isLoading() && !quiz()) {
        <div class="loading-container">
          <mat-spinner diameter="48"></mat-spinner>
          <p>Loading quiz...</p>
        </div>
      } @else if (quiz()) {
        <div class="run-start-container slide-up">
          <!-- Quiz Icon -->
          <div class="quiz-icon">
            <mat-icon>play_circle</mat-icon>
          </div>

          <!-- Quiz Info -->
          <h1>{{ quiz()!.name }}</h1>
          <p class="quiz-description">{{ quiz()!.description || 'Test your knowledge!' }}</p>

          <!-- Stats Card -->
          <div class="stats-card">
            <div class="stat">
              <mat-icon>help_outline</mat-icon>
              <div class="stat-info">
                <span class="stat-value">{{ quiz()!.questions_count }}</span>
                <span class="stat-label">Questions</span>
              </div>
            </div>
            <div class="stat-divider"></div>
            <div class="stat">
              <mat-icon>timer</mat-icon>
              <div class="stat-info">
                <span class="stat-value">~{{ estimatedTime() }}</span>
                <span class="stat-label">Minutes</span>
              </div>
            </div>
          </div>

          <!-- Tips -->
          <div class="tips-card">
            <h3>
              <mat-icon>lightbulb</mat-icon>
              Quick Tips
            </h3>
            <ul>
              <li>Read each question carefully</li>
              <li>You can't go back once you submit</li>
              <li>Take your time - no rush!</li>
            </ul>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <button 
              mat-raised-button 
              color="primary" 
              class="start-btn" 
              (click)="onStart()"
              [disabled]="isLoading()">
              @if (isLoading()) {
                <mat-spinner diameter="20"></mat-spinner>
              } @else {
                <mat-icon>play_arrow</mat-icon>
                Start Quiz
              }
            </button>
            <button mat-stroked-button routerLink="/app/quizzes" class="back-btn">
              <mat-icon>arrow_back</mat-icon>
              Back to Quizzes
            </button>
          </div>
        </div>
      }
    </div>
  `,
  styles: [`
    .run-start-page {
      min-height: calc(100vh - 64px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: var(--spacing-8);
      background: linear-gradient(135deg, var(--color-background) 0%, #e3f2fd 100%);
    }

    .loading-container {
      text-align: center;
    }

    .loading-container p {
      margin-top: var(--spacing-4);
      color: var(--color-text-secondary);
    }

    .run-start-container {
      text-align: center;
      max-width: 500px;
      width: 100%;
    }

    .quiz-icon {
      width: 100px;
      height: 100px;
      background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-bottom: var(--spacing-6);
      box-shadow: 0 10px 40px rgba(25, 118, 210, 0.3);
    }

    .quiz-icon mat-icon {
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

    .quiz-description {
      font-size: var(--font-size-body1);
      color: var(--color-text-secondary);
      margin-bottom: var(--spacing-8);
    }

    .stats-card {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: var(--spacing-8);
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      padding: var(--spacing-6);
      box-shadow: var(--shadow-md);
      margin-bottom: var(--spacing-6);
    }

    .stat {
      display: flex;
      align-items: center;
      gap: var(--spacing-3);
    }

    .stat mat-icon {
      font-size: 32px;
      width: 32px;
      height: 32px;
      color: var(--color-primary);
    }

    .stat-info {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
    }

    .stat-value {
      font-size: var(--font-size-h2);
      font-weight: var(--font-weight-bold);
      color: var(--color-text-primary);
    }

    .stat-label {
      font-size: var(--font-size-caption);
      color: var(--color-text-secondary);
    }

    .stat-divider {
      width: 1px;
      height: 48px;
      background: var(--color-divider);
    }

    .tips-card {
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      padding: var(--spacing-5);
      box-shadow: var(--shadow-sm);
      margin-bottom: var(--spacing-8);
      text-align: left;
    }

    .tips-card h3 {
      display: flex;
      align-items: center;
      gap: var(--spacing-2);
      font-size: var(--font-size-body1);
      margin-bottom: var(--spacing-3);
      color: var(--color-text-primary);
    }

    .tips-card h3 mat-icon {
      color: var(--color-warning);
      font-size: 20px;
      width: 20px;
      height: 20px;
    }

    .tips-card ul {
      margin: 0;
      padding-left: var(--spacing-6);
      color: var(--color-text-secondary);
      font-size: var(--font-size-body2);
    }

    .tips-card li {
      margin-bottom: var(--spacing-1);
    }

    .action-buttons {
      display: flex;
      flex-direction: column;
      gap: var(--spacing-3);
    }

    .start-btn {
      padding: var(--spacing-5) var(--spacing-8) !important;
      font-size: var(--font-size-h4) !important;
      border-radius: var(--radius-full) !important;
    }

    .start-btn mat-icon {
      margin-right: var(--spacing-2);
    }

    .back-btn {
      padding: var(--spacing-3) var(--spacing-6) !important;
      border-radius: var(--radius-full) !important;
    }

    .back-btn mat-icon {
      margin-right: var(--spacing-2);
    }

    @media (max-width: 600px) {
      .stats-card {
        flex-direction: column;
        gap: var(--spacing-4);
      }

      .stat-divider {
        width: 100%;
        height: 1px;
      }
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RunStartComponent implements OnInit {
  private quizService = inject(QuizService);
  private attemptRepo = inject(AttemptRepository);
  private appStateRepo = inject(AppStateRepository);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  isLoading = signal(false);
  quiz = signal<{ name: string; description: string; questions_count: number } | null>(null);
  quizId = 0;

  estimatedTime(): number {
    const q = this.quiz();
    if (!q) return 0;
    return Math.max(1, Math.ceil(q.questions_count * 0.5));
  }

  ngOnInit(): void {
    this.quizId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadQuiz();
  }

  loadQuiz(): void {
    this.isLoading.set(true);
    this.quizService.getQuiz(this.quizId).subscribe({
      next: (quiz) => {
        this.quiz.set(quiz);
        this.isLoading.set(false);
      },
      error: () => {
        this.isLoading.set(false);
      }
    });
  }

  async onStart(): Promise<void> {
    this.isLoading.set(true);
    try {
      const questions = await this.quizService.getQuestions(this.quizId).toPromise();
      if (!questions) throw new Error('No questions found');

      const questionIds = questions.map(q => q.id);
      const shuffled = this.shuffleArray([...questionIds]);
      const attemptId = await this.attemptRepo.createAttempt(this.quizId, shuffled);
      await this.appStateRepo.setActiveAttempt(this.quizId, attemptId);

      this.router.navigate(['/app/quizzes', this.quizId, 'run', 'q', 0]);
    } catch (error) {
      this.isLoading.set(false);
    }
  }

  private shuffleArray<T>(array: T[]): T[] {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }
}
