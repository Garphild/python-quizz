import { Component, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { TranslateModule } from '@ngx-translate/core';
import { AuthService } from '../../../core/services/auth.service';
import { LanguageSwitchComponent } from '../language-switch/language-switch.component';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatToolbarModule,
    MatButtonModule,
    MatMenuModule,
    MatIconModule,
    MatDividerModule,
    TranslateModule,
    LanguageSwitchComponent
  ],
  template: `
    <mat-toolbar class="header">
      <a routerLink="/" class="logo">
        <mat-icon class="logo-icon">school</mat-icon>
        <span class="logo-text">Quiz App</span>
      </a>

      <div class="spacer"></div>

      @if (authService.isAuthenticated()) {
        <nav class="nav-links">
          <a mat-button routerLink="/app/quizzes" routerLinkActive="active">
            <mat-icon>quiz</mat-icon>
            My Quizzes
          </a>
        </nav>

        <button mat-button [matMenuTriggerFor]="userMenu" class="user-menu-trigger">
          <div class="user-avatar">
            {{ getInitials() }}
          </div>
          <span class="user-name">{{ authService.currentUser()?.name }}</span>
          <mat-icon>expand_more</mat-icon>
        </button>
        
        <mat-menu #userMenu="matMenu" class="user-menu">
          <div class="menu-header">
            <div class="menu-avatar">{{ getInitials() }}</div>
            <div class="menu-info">
              <span class="menu-name">{{ authService.currentUser()?.name }}</span>
              <span class="menu-email">{{ authService.currentUser()?.email }}</span>
            </div>
          </div>
          <mat-divider></mat-divider>
          <button mat-menu-item routerLink="/app/profile">
            <mat-icon>person</mat-icon>
            <span>{{ 'AUTH.PROFILE' | translate }}</span>
          </button>
          <mat-divider></mat-divider>
          <button mat-menu-item (click)="logout()" class="logout-item">
            <mat-icon>logout</mat-icon>
            <span>{{ 'AUTH.LOGOUT' | translate }}</span>
          </button>
        </mat-menu>
      }
      
      <app-language-switch></app-language-switch>
    </mat-toolbar>
  `,
  styles: [`
    .header {
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 0 var(--spacing-6);
      box-shadow: var(--shadow-sm);
    }

    .logo {
      display: flex;
      align-items: center;
      gap: var(--spacing-2);
      text-decoration: none;
      color: white;
    }

    .logo-icon {
      font-size: 28px;
      width: 28px;
      height: 28px;
    }

    .logo-text {
      font-size: var(--font-size-h4);
      font-weight: var(--font-weight-bold);
      letter-spacing: 0.5px;
    }

    .spacer {
      flex: 1 1 auto;
    }

    .nav-links {
      display: flex;
      gap: var(--spacing-2);
      margin-right: var(--spacing-4);
    }

    .nav-links a {
      color: rgba(255, 255, 255, 0.9);
      transition: all var(--transition-fast);
    }

    .nav-links a:hover {
      color: white;
      background: rgba(255, 255, 255, 0.1);
    }

    .nav-links a.active {
      color: white;
      background: rgba(255, 255, 255, 0.15);
    }

    .nav-links mat-icon {
      margin-right: var(--spacing-1);
    }

    .user-menu-trigger {
      display: flex;
      align-items: center;
      gap: var(--spacing-2);
      padding: var(--spacing-1) var(--spacing-3);
      border-radius: var(--radius-full);
      color: white;
    }

    .user-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: var(--font-size-caption);
      font-weight: var(--font-weight-bold);
    }

    .user-name {
      max-width: 120px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .menu-header {
      display: flex;
      align-items: center;
      gap: var(--spacing-3);
      padding: var(--spacing-4);
    }

    .menu-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: var(--color-primary);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: var(--font-weight-bold);
    }

    .menu-info {
      display: flex;
      flex-direction: column;
    }

    .menu-name {
      font-weight: var(--font-weight-medium);
      color: var(--color-text-primary);
    }

    .menu-email {
      font-size: var(--font-size-caption);
      color: var(--color-text-secondary);
    }

    .logout-item {
      color: var(--color-error);
    }

    .logout-item mat-icon {
      color: var(--color-error);
    }

    @media (max-width: 768px) {
      .nav-links {
        display: none;
      }

      .user-name {
        display: none;
      }
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HeaderComponent {
  authService = inject(AuthService);
  private router = inject(Router);

  getInitials(): string {
    const user = this.authService.currentUser();
    if (!user) return '?';
    const first = user.name?.charAt(0) || '';
    const last = user.surname?.charAt(0) || '';
    return (first + last).toUpperCase() || user.email.charAt(0).toUpperCase();
  }

  logout(): void {
    this.authService.logout().subscribe(() => {
      this.authService.setCurrentUser(null);
      this.router.navigate(['/']);
    });
  }
}
