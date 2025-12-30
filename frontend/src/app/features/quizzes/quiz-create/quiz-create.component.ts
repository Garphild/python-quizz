import { Component, inject, ChangeDetectionStrategy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { TranslateModule } from '@ngx-translate/core';
import { QuizService } from '../../../core/services/quiz.service';
import { NotificationService } from '../../../core/services/notification.service';

@Component({
  selector: 'app-quiz-create',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatIconModule,
    TranslateModule
  ],
  template: `
    <div class="create-page">
      <div class="create-container slide-up">
        <!-- Header Icon -->
        <div class="create-icon">
          <mat-icon>add_circle</mat-icon>
        </div>

        <h1>{{ 'QUIZ.CREATE' | translate }}</h1>
        <p class="subtitle">{{ 'QUIZ.CREATE_SUBTITLE' | translate }}</p>

        <!-- Create Card -->
        <div class="create-card">
          <form [formGroup]="form" (ngSubmit)="onSubmit()">
            <div class="input-section">
              <mat-form-field appearance="outline" class="url-field">
                <mat-label>{{ 'QUIZ.YOUTUBE_URL' | translate }}</mat-label>
                <mat-icon matPrefix>link</mat-icon>
                <input matInput formControlName="url" placeholder="https://www.youtube.com/watch?v=...">
                @if (form.get('url')?.hasError('required')) {
                  <mat-error>{{ 'ERRORS.REQUIRED' | translate }}</mat-error>
                }
                @if (form.get('url')?.hasError('pattern')) {
                  <mat-error>{{ 'ERRORS.INVALID_FORMAT' | translate }}</mat-error>
                }
              </mat-form-field>
            </div>

            <!-- How it works -->
            <div class="how-it-works">
              <h3>
                <mat-icon>auto_awesome</mat-icon>
                {{ 'QUIZ.HOW_IT_WORKS' | translate }}
              </h3>
              <div class="steps">
                <div class="step">
                  <div class="step-num">1</div>
                  <span>{{ 'QUIZ.STEP_1' | translate }}</span>
                </div>
                <div class="step">
                  <div class="step-num">2</div>
                  <span>{{ 'QUIZ.STEP_2' | translate }}</span>
                </div>
                <div class="step">
                  <div class="step-num">3</div>
                  <span>{{ 'QUIZ.STEP_3' | translate }}</span>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-buttons">
              <button 
                mat-raised-button 
                color="primary" 
                type="submit"
                class="create-btn"
                [disabled]="form.invalid || isLoading()">
                @if (isLoading()) {
                  <ng-container>
                    <mat-spinner diameter="20"></mat-spinner>
                    <span>{{ 'QUIZ.GENERATING' | translate }}</span>
                  </ng-container>
                } @else {
                  <ng-container>
                    <mat-icon>auto_awesome</mat-icon>
                    {{ 'QUIZ.GENERATE' | translate }}
                  </ng-container>
                }
              </button>
              <button mat-stroked-button type="button" routerLink="/app/quizzes" class="cancel-btn">
                {{ 'COMMON.CANCEL' | translate }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .create-page {
      min-height: calc(100vh - 64px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: var(--spacing-8);
      background: linear-gradient(135deg, var(--color-background) 0%, #e3f2fd 100%);
    }

    .create-container {
      text-align: center;
      max-width: 520px;
      width: 100%;
    }

    .create-icon {
      width: 80px;
      height: 80px;
      background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-bottom: var(--spacing-5);
      box-shadow: 0 10px 40px rgba(25, 118, 210, 0.3);
    }

    .create-icon mat-icon {
      font-size: 40px;
      width: 40px;
      height: 40px;
      color: white;
    }

    h1 {
      font-size: var(--font-size-h1);
      font-weight: var(--font-weight-bold);
      margin-bottom: var(--spacing-2);
      color: var(--color-text-primary);
    }

    .subtitle {
      font-size: var(--font-size-body1);
      color: var(--color-text-secondary);
      margin-bottom: var(--spacing-8);
    }

    .create-card {
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      padding: var(--spacing-8);
      box-shadow: var(--shadow-lg);
      text-align: left;
    }

    .url-field {
      width: 100%;
    }

    mat-icon[matPrefix] {
      color: var(--color-text-secondary);
      margin-right: var(--spacing-2);
    }

    .how-it-works {
      background: var(--color-background);
      border-radius: var(--radius-md);
      padding: var(--spacing-5);
      margin: var(--spacing-6) 0;
    }

    .how-it-works h3 {
      display: flex;
      align-items: center;
      gap: var(--spacing-2);
      font-size: var(--font-size-body1);
      font-weight: var(--font-weight-medium);
      margin-bottom: var(--spacing-4);
      color: var(--color-text-primary);
    }

    .how-it-works h3 mat-icon {
      color: var(--color-accent);
      font-size: 20px;
      width: 20px;
      height: 20px;
    }

    .steps {
      display: flex;
      flex-direction: column;
      gap: var(--spacing-3);
    }

    .step {
      display: flex;
      align-items: center;
      gap: var(--spacing-3);
      color: var(--color-text-secondary);
      font-size: var(--font-size-body2);
    }

    .step-num {
      width: 24px;
      height: 24px;
      background: var(--color-primary);
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: var(--font-size-caption);
      font-weight: var(--font-weight-bold);
      flex-shrink: 0;
    }

    .action-buttons {
      display: flex;
      flex-direction: column;
      gap: var(--spacing-3);
    }

    .create-btn {
      width: 100%;
      padding: var(--spacing-4) !important;
      font-size: var(--font-size-body1) !important;
      border-radius: var(--radius-md) !important;
    }

    .create-btn mat-icon,
    .create-btn mat-spinner {
      margin-right: var(--spacing-2);
    }

    .cancel-btn {
      width: 100%;
      padding: var(--spacing-3) !important;
      border-radius: var(--radius-md) !important;
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class QuizCreateComponent {
  private quizService = inject(QuizService);
  private notification = inject(NotificationService);
  private router = inject(Router);
  private fb = inject(FormBuilder);

  isLoading = signal(false);
  form = this.fb.group({
    url: ['', [
      Validators.required,
      Validators.pattern(/^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]+/)
    ]]
  });

  onSubmit(): void {
    if (this.form.invalid) {
      return;
    }

    this.isLoading.set(true);
    const data = this.form.getRawValue() as any;

    this.quizService.createQuiz(data).subscribe({
      next: () => {
        this.notification.success('Quiz created successfully');
        this.router.navigate(['/app/quizzes']);
      },
      error: () => {
        this.isLoading.set(false);
      }
    });
  }
}
