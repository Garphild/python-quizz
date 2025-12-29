import { Component, inject, ChangeDetectionStrategy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router, ActivatedRoute } from '@angular/router';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { TranslateModule } from '@ngx-translate/core';
import { AuthService } from '../../../core/services/auth.service';
import { NotificationService } from '../../../core/services/notification.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatIconModule,
    TranslateModule
  ],
  template: `
    <div class="auth-page">
      <div class="auth-container slide-up">
        <div class="auth-header">
          <div class="auth-icon">
            <mat-icon>login</mat-icon>
          </div>
          <h1>{{ 'AUTH.LOGIN' | translate }}</h1>
          <p>Welcome back! Sign in to continue.</p>
        </div>

        <mat-card class="auth-card">
          <mat-card-content>
            <form [formGroup]="form" (ngSubmit)="onSubmit()">
              <mat-form-field appearance="outline">
                <mat-label>{{ 'COMMON.EMAIL' | translate }}</mat-label>
                <mat-icon matPrefix>email</mat-icon>
                <input matInput type="email" formControlName="email" autocomplete="email">
                @if (form.get('email')?.hasError('required')) {
                  <mat-error>{{ 'ERRORS.REQUIRED' | translate }}</mat-error>
                }
                @if (form.get('email')?.hasError('email')) {
                  <mat-error>{{ 'ERRORS.INVALID_EMAIL' | translate }}</mat-error>
                }
              </mat-form-field>

              <mat-form-field appearance="outline">
                <mat-label>{{ 'COMMON.PASSWORD' | translate }}</mat-label>
                <mat-icon matPrefix>lock</mat-icon>
                <input matInput [type]="hidePassword() ? 'password' : 'text'" formControlName="password" autocomplete="current-password">
                <button mat-icon-button matSuffix type="button" (click)="hidePassword.set(!hidePassword())">
                  <mat-icon>{{ hidePassword() ? 'visibility_off' : 'visibility' }}</mat-icon>
                </button>
                @if (form.get('password')?.hasError('required')) {
                  <mat-error>{{ 'ERRORS.REQUIRED' | translate }}</mat-error>
                }
              </mat-form-field>

              <button 
                mat-raised-button 
                color="primary" 
                type="submit"
                class="submit-button"
                [disabled]="form.invalid || isLoading()">
                @if (isLoading()) {
                  <mat-spinner diameter="20"></mat-spinner>
                } @else {
                  <mat-icon>arrow_forward</mat-icon>
                  {{ 'AUTH.LOGIN' | translate }}
                }
              </button>
            </form>

            <div class="auth-divider">
              <span>or</span>
            </div>

            <p class="auth-link">
              {{ 'AUTH.NO_ACCOUNT' | translate }}
              <a routerLink="/auth/register">{{ 'AUTH.REGISTER' | translate }}</a>
            </p>
          </mat-card-content>
        </mat-card>

        <a routerLink="/" class="back-link">
          <mat-icon>arrow_back</mat-icon>
          Back to home
        </a>
      </div>
    </div>
  `,
  styles: [`
    .auth-page {
      min-height: calc(100vh - 64px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: var(--spacing-8);
      background: linear-gradient(135deg, var(--color-background) 0%, #e3f2fd 100%);
    }

    .auth-container {
      width: 100%;
      max-width: 420px;
    }

    .auth-header {
      text-align: center;
      margin-bottom: var(--spacing-6);
    }

    .auth-icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 64px;
      height: 64px;
      background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
      border-radius: 50%;
      margin-bottom: var(--spacing-4);
      box-shadow: 0 8px 24px rgba(25, 118, 210, 0.3);
    }

    .auth-icon mat-icon {
      font-size: 32px;
      width: 32px;
      height: 32px;
      color: white;
    }

    .auth-header h1 {
      font-size: var(--font-size-h2);
      font-weight: var(--font-weight-bold);
      margin-bottom: var(--spacing-2);
      color: var(--color-text-primary);
    }

    .auth-header p {
      color: var(--color-text-secondary);
      margin: 0;
    }

    .auth-card {
      border-radius: var(--radius-lg) !important;
      box-shadow: var(--shadow-lg) !important;
      padding: var(--spacing-6);
    }

    mat-form-field {
      width: 100%;
      margin-bottom: var(--spacing-2);
    }

    mat-icon[matPrefix] {
      color: var(--color-text-secondary);
      margin-right: var(--spacing-2);
    }

    .submit-button {
      width: 100%;
      padding: var(--spacing-4) !important;
      font-size: var(--font-size-body1) !important;
      border-radius: var(--radius-md) !important;
      margin-top: var(--spacing-4);
    }

    .submit-button mat-icon {
      margin-right: var(--spacing-2);
    }

    .auth-divider {
      display: flex;
      align-items: center;
      margin: var(--spacing-6) 0;
      color: var(--color-text-secondary);
    }

    .auth-divider::before,
    .auth-divider::after {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--color-divider);
    }

    .auth-divider span {
      padding: 0 var(--spacing-4);
      font-size: var(--font-size-caption);
      text-transform: uppercase;
    }

    .auth-link {
      text-align: center;
      color: var(--color-text-secondary);
      margin: 0;
    }

    .auth-link a {
      color: var(--color-primary);
      font-weight: var(--font-weight-medium);
      margin-left: var(--spacing-1);
    }

    .auth-link a:hover {
      text-decoration: underline;
    }

    .back-link {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--spacing-2);
      margin-top: var(--spacing-6);
      color: var(--color-text-secondary);
      font-size: var(--font-size-body2);
      transition: color var(--transition-fast);
    }

    .back-link:hover {
      color: var(--color-primary);
    }

    .back-link mat-icon {
      font-size: 18px;
      width: 18px;
      height: 18px;
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginComponent {
  private authService = inject(AuthService);
  private notificationService = inject(NotificationService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private fb = inject(FormBuilder);

  isLoading = signal(false);
  hidePassword = signal(true);

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required]
  });

  onSubmit(): void {
    if (this.form.invalid) return;

    this.isLoading.set(true);
    const { email, password } = this.form.value;

    this.authService.login({ email: email!, password: password! }).subscribe({
      next: (profile) => {
        this.authService.currentUser.set(profile);
        const returnUrl = this.route.snapshot.queryParamMap.get('returnUrl') || '/app/quizzes';
        this.router.navigate([returnUrl]);
      },
      error: () => {
        this.isLoading.set(false);
        this.notificationService.error('ERRORS.LOGIN_FAILED');
      }
    });
  }
}
