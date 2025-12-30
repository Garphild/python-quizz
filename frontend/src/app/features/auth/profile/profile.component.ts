import { Component, inject, ChangeDetectionStrategy, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { TranslateModule } from '@ngx-translate/core';
import { AuthService } from '../../../core/services/auth.service';
import { NotificationService } from '../../../core/services/notification.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatTabsModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatDividerModule,
    TranslateModule
  ],
  template: `
    <div class="profile-page">
      <div class="profile-container">
        <!-- Profile Header -->
        <div class="profile-header">
          <div class="avatar">
            {{ getInitials() }}
          </div>
          <div class="user-info">
            <h1>{{ authService.currentUser()?.name }} {{ authService.currentUser()?.surname }}</h1>
            <p>{{ authService.currentUser()?.email }}</p>
          </div>
        </div>

        <!-- Profile Content -->
        <div class="profile-card">
          <mat-tab-group>
            <mat-tab>
              <ng-template mat-tab-label>
                <mat-icon>person</mat-icon>
                <span>{{ 'AUTH.PROFILE' | translate }}</span>
              </ng-template>
              <div class="tab-content">
                <form [formGroup]="profileForm" (ngSubmit)="onUpdateProfile()">
                  <mat-form-field appearance="outline">
                    <mat-label>{{ 'AUTH.EMAIL' | translate }}</mat-label>
                    <mat-icon matPrefix>email</mat-icon>
                    <input matInput type="email" [value]="authService.currentUser()?.email" disabled>
                  </mat-form-field>

                  <div class="form-row">
                    <mat-form-field appearance="outline">
                      <mat-label>{{ 'AUTH.NAME' | translate }}</mat-label>
                      <mat-icon matPrefix>person</mat-icon>
                      <input matInput formControlName="name">
                    </mat-form-field>

                    <mat-form-field appearance="outline">
                      <mat-label>{{ 'AUTH.SURNAME' | translate }}</mat-label>
                      <input matInput formControlName="surname">
                    </mat-form-field>
                  </div>

                  <button mat-raised-button color="primary" type="submit" class="save-btn" [disabled]="profileForm.invalid || isLoading()">
                    @if (isLoading()) {
                      <mat-spinner diameter="20"></mat-spinner>
                    } @else {
                      <ng-container>
                        <mat-icon>save</mat-icon>
                        {{ 'COMMON.SAVE' | translate }}
                      </ng-container>
                    }
                  </button>
                </form>
              </div>
            </mat-tab>

            <mat-tab>
              <ng-template mat-tab-label>
                <mat-icon>lock</mat-icon>
                <span>{{ 'PROFILE.SECURITY' | translate }}</span>
              </ng-template>
              <div class="tab-content">
                <h3>{{ 'PROFILE.CHANGE_PASSWORD' | translate }}</h3>
                <form [formGroup]="passwordForm" (ngSubmit)="onChangePassword()">
                  <mat-form-field appearance="outline">
                    <mat-label>{{ 'AUTH.OLD_PASSWORD' | translate }}</mat-label>
                    <mat-icon matPrefix>lock</mat-icon>
                    <input matInput [type]="hideOldPwd() ? 'password' : 'text'" formControlName="old_password">
                    <button mat-icon-button matSuffix type="button" (click)="hideOldPwd.set(!hideOldPwd())">
                      <mat-icon>{{ hideOldPwd() ? 'visibility_off' : 'visibility' }}</mat-icon>
                    </button>
                  </mat-form-field>

                  <mat-form-field appearance="outline">
                    <mat-label>{{ 'AUTH.NEW_PASSWORD' | translate }}</mat-label>
                    <mat-icon matPrefix>lock_outline</mat-icon>
                    <input matInput [type]="hideNewPwd() ? 'password' : 'text'" formControlName="new_password">
                    <button mat-icon-button matSuffix type="button" (click)="hideNewPwd.set(!hideNewPwd())">
                      <mat-icon>{{ hideNewPwd() ? 'visibility_off' : 'visibility' }}</mat-icon>
                    </button>
                    <mat-hint>{{ 'PROFILE.MIN_8_CHARS' | translate }}</mat-hint>
                  </mat-form-field>

                  <button mat-raised-button color="primary" type="submit" class="save-btn" [disabled]="passwordForm.invalid || isLoading()">
                    @if (isLoading()) {
                      <mat-spinner diameter="20"></mat-spinner>
                    } @else {
                      <ng-container>
                        <mat-icon>lock_reset</mat-icon>
                        {{ 'PROFILE.UPDATE_PASSWORD' | translate }}
                      </ng-container>
                    }
                  </button>
                </form>
              </div>
            </mat-tab>
          </mat-tab-group>

          <mat-divider></mat-divider>

          <div class="logout-section">
            <button mat-stroked-button color="warn" (click)="onLogout()">
              <mat-icon>logout</mat-icon>
              {{ 'AUTH.LOGOUT' | translate }}
            </button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .profile-page {
      min-height: calc(100vh - 64px);
      padding: var(--spacing-8);
      background: linear-gradient(135deg, var(--color-background) 0%, #e3f2fd 100%);
    }

    .profile-container {
      max-width: 600px;
      margin: 0 auto;
    }

    .profile-header {
      display: flex;
      align-items: center;
      gap: var(--spacing-6);
      margin-bottom: var(--spacing-8);
    }

    .avatar {
      width: 80px;
      height: 80px;
      background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: var(--font-size-h2);
      font-weight: var(--font-weight-bold);
      color: white;
      box-shadow: 0 8px 24px rgba(25, 118, 210, 0.3);
    }

    .user-info h1 {
      font-size: var(--font-size-h2);
      font-weight: var(--font-weight-bold);
      margin: 0 0 var(--spacing-1) 0;
      color: var(--color-text-primary);
    }

    .user-info p {
      font-size: var(--font-size-body1);
      color: var(--color-text-secondary);
      margin: 0;
    }

    .profile-card {
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-lg);
      overflow: hidden;
    }

    mat-tab-group {
      padding: 0;
    }

    ::ng-deep .mat-mdc-tab .mdc-tab__text-label {
      display: flex;
      align-items: center;
      gap: var(--spacing-2);
    }

    .tab-content {
      padding: var(--spacing-6);
    }

    .tab-content h3 {
      font-size: var(--font-size-h4);
      margin-bottom: var(--spacing-5);
      color: var(--color-text-primary);
    }

    mat-form-field {
      width: 100%;
      margin-bottom: var(--spacing-3);
    }

    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--spacing-4);
    }

    mat-icon[matPrefix] {
      color: var(--color-text-secondary);
      margin-right: var(--spacing-2);
    }

    .save-btn {
      width: 100%;
      padding: var(--spacing-4) !important;
      margin-top: var(--spacing-4);
      border-radius: var(--radius-md) !important;
    }

    .save-btn mat-icon {
      margin-right: var(--spacing-2);
    }

    .logout-section {
      padding: var(--spacing-6);
      text-align: center;
    }

    .logout-section button {
      padding: var(--spacing-3) var(--spacing-8) !important;
      border-radius: var(--radius-md) !important;
    }

    .logout-section button mat-icon {
      margin-right: var(--spacing-2);
    }

    @media (max-width: 600px) {
      .profile-header {
        flex-direction: column;
        text-align: center;
      }

      .form-row {
        grid-template-columns: 1fr;
      }
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProfileComponent implements OnInit {
  authService = inject(AuthService);
  private notification = inject(NotificationService);
  private router = inject(Router);
  private fb = inject(FormBuilder);

  isLoading = signal(false);
  hideOldPwd = signal(true);
  hideNewPwd = signal(true);

  getInitials(): string {
    const user = this.authService.currentUser();
    if (!user) return '?';
    const first = user.name?.charAt(0) || '';
    const last = user.surname?.charAt(0) || '';
    return (first + last).toUpperCase() || user.email.charAt(0).toUpperCase();
  }

  profileForm = this.fb.group({
    name: ['', [Validators.required, Validators.minLength(2)]],
    surname: ['']
  });

  passwordForm = this.fb.group({
    old_password: ['', Validators.required],
    new_password: ['', [Validators.required, Validators.minLength(8)]]
  });

  ngOnInit(): void {
    const user = this.authService.currentUser();
    if (user) {
      this.profileForm.patchValue({
        name: user.name,
        surname: user.surname
      });
    }
  }

  onUpdateProfile(): void {
    if (this.profileForm.invalid) {
      return;
    }

    this.isLoading.set(true);
    const data = this.profileForm.getRawValue() as any;

    this.authService.updateProfile(data).subscribe({
      next: (profile) => {
        this.authService.currentUser.set(profile);
        this.notification.success('Profile updated');
        this.isLoading.set(false);
      },
      error: () => {
        this.isLoading.set(false);
      }
    });
  }

  onChangePassword(): void {
    if (this.passwordForm.invalid) {
      return;
    }

    this.isLoading.set(true);
    const data = this.passwordForm.getRawValue() as any;

    this.authService.changePassword(data).subscribe({
      next: () => {
        this.notification.success('Password changed');
        this.passwordForm.reset();
        this.isLoading.set(false);
      },
      error: () => {
        this.isLoading.set(false);
      }
    });
  }

  onLogout(): void {
    this.authService.logout().subscribe(() => {
      this.authService.currentUser.set(null);
      this.router.navigate(['/']);
    });
  }
}
