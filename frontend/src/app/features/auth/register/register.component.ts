import { Component, inject, ChangeDetectionStrategy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
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
  selector: 'app-register',
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
    <div class="auth-page">
      <div class="auth-container slide-up">
        <div class="auth-header">
          <div class="auth-icon">
            <mat-icon>person_add</mat-icon>
          </div>
          <h1>{{ 'AUTH.REGISTER' | translate }}</h1>
          <p>Create your account to get started</p>
        </div>

        <mat-card class="auth-card">
          <mat-card-content>
            <form [formGroup]="form" (ngSubmit)="onSubmit()">
              <div class="form-row">
                <mat-form-field appearance="outline">
                  <mat-label>{{ 'AUTH.NAME' | translate }}</mat-label>
                  <mat-icon matPrefix>person</mat-icon>
                  <input matInput formControlName="name" autocomplete="given-name">
                  @if (form.get('name')?.hasError('required')) {
                    <mat-error>{{ 'ERRORS.REQUIRED' | translate }}</mat-error>
                  }
                </mat-form-field>

                <mat-form-field appearance="outline">
                  <mat-label>{{ 'AUTH.SURNAME' | translate }}</mat-label>
                  <input matInput formControlName="surname" autocomplete="family-name">
                </mat-form-field>
              </div>

              <mat-form-field appearance="outline">
                <mat-label>{{ 'AUTH.EMAIL' | translate }}</mat-label>
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
                <mat-label>{{ 'AUTH.PASSWORD' | translate }}</mat-label>
                <mat-icon matPrefix>lock</mat-icon>
                <input matInput [type]="hidePassword() ? 'password' : 'text'" formControlName="password" autocomplete="new-password">
                <button mat-icon-button matSuffix type="button" (click)="hidePassword.set(!hidePassword())">
                  <mat-icon>{{ hidePassword() ? 'visibility_off' : 'visibility' }}</mat-icon>
                </button>
                @if (form.get('password')?.hasError('required')) {
                  <mat-error>{{ 'ERRORS.REQUIRED' | translate }}</mat-error>
                }
                @if (form.get('password')?.hasError('minlength')) {
                  <mat-error>Min 8 characters</mat-error>
                }
              </mat-form-field>

              <mat-form-field appearance="outline">
                <mat-label>{{ 'AUTH.CONFIRM_PASSWORD' | translate }}</mat-label>
                <mat-icon matPrefix>lock_outline</mat-icon>
                <input matInput [type]="hideConfirmPassword() ? 'password' : 'text'" formControlName="confirmPassword" autocomplete="new-password">
                <button mat-icon-button matSuffix type="button" (click)="hideConfirmPassword.set(!hideConfirmPassword())">
                  <mat-icon>{{ hideConfirmPassword() ? 'visibility_off' : 'visibility' }}</mat-icon>
                </button>
                @if (form.get('confirmPassword')?.hasError('required')) {
                  <mat-error>{{ 'ERRORS.REQUIRED' | translate }}</mat-error>
                }
                @if (form.hasError('passwordMismatch')) {
                  <mat-error>Passwords do not match</mat-error>
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
                  <mat-icon>how_to_reg</mat-icon>
                  {{ 'AUTH.REGISTER' | translate }}
                }
              </button>
            </form>

            <div class="auth-divider">
              <span>or</span>
            </div>

            <p class="auth-link">
              Already have an account?
              <a routerLink="/auth/login">{{ 'AUTH.LOGIN' | translate }}</a>
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
      max-width: 480px;
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

    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--spacing-4);
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

    @media (max-width: 600px) {
      .form-row {
        grid-template-columns: 1fr;
      }
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RegisterComponent {
  private authService = inject(AuthService);
  private notification = inject(NotificationService);
  private router = inject(Router);
  private fb = inject(FormBuilder);

  isLoading = signal(false);
  hidePassword = signal(true);
  hideConfirmPassword = signal(true);

  form = this.fb.group(
    {
      name: ['', [Validators.required, Validators.minLength(2)]],
      surname: [''],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required]
    },
    { validators: this.passwordMatchValidator }
  );

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('password');
    const confirmPassword = control.get('confirmPassword');

    if (!password || !confirmPassword) {
      return null;
    }

    return password.value === confirmPassword.value ? null : { passwordMismatch: true };
  }

  onSubmit(): void {
    if (this.form.invalid) {
      return;
    }

    this.isLoading.set(true);
    const { confirmPassword, ...data } = this.form.getRawValue() as any;

    this.authService.register(data).subscribe({
      next: () => {
        this.notification.success('Registration successful. Please login.');
        this.router.navigate(['/auth/login']);
      },
      error: () => {
        this.isLoading.set(false);
      }
    });
  }
}
