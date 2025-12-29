import { Component, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { TranslateModule } from '@ngx-translate/core';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, RouterModule, MatButtonModule, MatIconModule, TranslateModule],
  template: `
    <div class="landing-page">
      <!-- Hero Section -->
      <section class="hero">
        <div class="hero-content slide-up">
          <div class="hero-icon">
            <mat-icon>school</mat-icon>
          </div>
          <h1 class="hero-title">Quiz App</h1>
          <p class="hero-subtitle">
            Transform YouTube videos into interactive quizzes with AI-powered question generation
          </p>
          
          <div class="hero-features">
            <div class="feature">
              <mat-icon>smart_toy</mat-icon>
              <span>AI-Powered</span>
            </div>
            <div class="feature">
              <mat-icon>youtube_searched_for</mat-icon>
              <span>From YouTube</span>
            </div>
            <div class="feature">
              <mat-icon>quiz</mat-icon>
              <span>Interactive</span>
            </div>
          </div>

          @if (authService.isAuthenticated()) {
            <div class="cta-buttons">
              <button mat-raised-button color="primary" class="cta-primary" routerLink="/app/quizzes">
                <mat-icon>arrow_forward</mat-icon>
                Go to Dashboard
              </button>
            </div>
          } @else {
            <div class="cta-buttons">
              <button mat-raised-button color="primary" class="cta-primary" routerLink="/auth/register">
                <mat-icon>person_add</mat-icon>
                Get Started Free
              </button>
              <button mat-stroked-button color="primary" class="cta-secondary" routerLink="/auth/login">
                <mat-icon>login</mat-icon>
                Sign In
              </button>
            </div>
          }
        </div>

        <!-- Decorative Background -->
        <div class="hero-bg">
          <div class="circle circle-1"></div>
          <div class="circle circle-2"></div>
          <div class="circle circle-3"></div>
        </div>
      </section>

      <!-- How It Works -->
      <section class="how-it-works">
        <h2>How It Works</h2>
        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <mat-icon>link</mat-icon>
            <h3>Paste YouTube URL</h3>
            <p>Simply paste a link to any educational YouTube video</p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <mat-icon>psychology</mat-icon>
            <h3>AI Generates Quiz</h3>
            <p>Our AI analyzes the video and creates relevant questions</p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <mat-icon>emoji_events</mat-icon>
            <h3>Learn & Track</h3>
            <p>Take quizzes, get instant feedback, track your progress</p>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="landing-footer">
        <p>&copy; 2024 Quiz App. Learn smarter, not harder.</p>
      </footer>
    </div>
  `,
  styles: [`
    .landing-page {
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* Hero Section */
    .hero {
      position: relative;
      min-height: calc(100vh - 64px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: var(--spacing-8);
      overflow: hidden;
    }

    .hero-content {
      position: relative;
      z-index: 2;
      text-align: center;
      max-width: 700px;
    }

    .hero-icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 100px;
      height: 100px;
      background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
      border-radius: 50%;
      margin-bottom: var(--spacing-6);
      box-shadow: 0 10px 40px rgba(25, 118, 210, 0.3);
    }

    .hero-icon mat-icon {
      font-size: 48px;
      width: 48px;
      height: 48px;
      color: white;
    }

    .hero-title {
      font-size: var(--font-size-display);
      font-weight: var(--font-weight-bold);
      background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: var(--spacing-4);
    }

    .hero-subtitle {
      font-size: var(--font-size-h3);
      color: var(--color-text-secondary);
      margin-bottom: var(--spacing-8);
      line-height: 1.6;
    }

    .hero-features {
      display: flex;
      justify-content: center;
      gap: var(--spacing-8);
      margin-bottom: var(--spacing-8);
      flex-wrap: wrap;
    }

    .feature {
      display: flex;
      align-items: center;
      gap: var(--spacing-2);
      color: var(--color-text-secondary);
      font-weight: var(--font-weight-medium);
    }

    .feature mat-icon {
      color: var(--color-primary);
    }

    .cta-buttons {
      display: flex;
      gap: var(--spacing-4);
      justify-content: center;
      flex-wrap: wrap;
    }

    .cta-primary {
      padding: var(--spacing-4) var(--spacing-8) !important;
      font-size: var(--font-size-body1) !important;
      border-radius: var(--radius-full) !important;
    }

    .cta-secondary {
      padding: var(--spacing-4) var(--spacing-8) !important;
      font-size: var(--font-size-body1) !important;
      border-radius: var(--radius-full) !important;
    }

    .cta-primary mat-icon,
    .cta-secondary mat-icon {
      margin-right: var(--spacing-2);
    }

    /* Decorative Background */
    .hero-bg {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 1;
      overflow: hidden;
    }

    .circle {
      position: absolute;
      border-radius: 50%;
      opacity: 0.1;
    }

    .circle-1 {
      width: 600px;
      height: 600px;
      background: var(--color-primary);
      top: -200px;
      right: -200px;
    }

    .circle-2 {
      width: 400px;
      height: 400px;
      background: var(--color-accent);
      bottom: -100px;
      left: -100px;
    }

    .circle-3 {
      width: 200px;
      height: 200px;
      background: var(--color-primary-light);
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }

    /* How It Works Section */
    .how-it-works {
      padding: var(--spacing-16) var(--spacing-8);
      background: var(--color-surface);
    }

    .how-it-works h2 {
      text-align: center;
      font-size: var(--font-size-h1);
      margin-bottom: var(--spacing-12);
      color: var(--color-text-primary);
    }

    .steps {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: var(--spacing-8);
      max-width: 1200px;
      margin: 0 auto;
    }

    .step {
      text-align: center;
      padding: var(--spacing-8);
      border-radius: var(--radius-lg);
      background: var(--color-background);
      position: relative;
      transition: transform var(--transition-normal), box-shadow var(--transition-normal);
    }

    .step:hover {
      transform: translateY(-5px);
      box-shadow: var(--shadow-lg);
    }

    .step-number {
      position: absolute;
      top: var(--spacing-4);
      left: var(--spacing-4);
      width: 32px;
      height: 32px;
      background: var(--color-primary);
      color: white;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: var(--font-weight-bold);
      font-size: var(--font-size-body2);
    }

    .step mat-icon {
      font-size: 48px;
      width: 48px;
      height: 48px;
      color: var(--color-primary);
      margin-bottom: var(--spacing-4);
    }

    .step h3 {
      font-size: var(--font-size-h4);
      margin-bottom: var(--spacing-2);
      color: var(--color-text-primary);
    }

    .step p {
      color: var(--color-text-secondary);
      font-size: var(--font-size-body2);
      margin: 0;
    }

    /* Footer */
    .landing-footer {
      padding: var(--spacing-8);
      text-align: center;
      background: var(--color-text-primary);
      color: white;
    }

    .landing-footer p {
      color: rgba(255, 255, 255, 0.7);
      margin: 0;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .hero-title {
        font-size: 2.5rem;
      }

      .hero-subtitle {
        font-size: var(--font-size-body1);
      }

      .hero-features {
        gap: var(--spacing-4);
      }

      .cta-buttons {
        flex-direction: column;
        align-items: center;
      }

      .cta-primary,
      .cta-secondary {
        width: 100%;
        max-width: 300px;
      }
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LandingComponent {
  authService = inject(AuthService);
}
