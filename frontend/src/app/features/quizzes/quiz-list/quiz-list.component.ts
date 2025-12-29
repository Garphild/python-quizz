import { Component, inject, ChangeDetectionStrategy, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialog } from '@angular/material/dialog';
import { TranslateModule } from '@ngx-translate/core';
import { QuizService } from '../../../core/services/quiz.service';
import { NotificationService } from '../../../core/services/notification.service';
import { QuizzDto } from '../../../core/models/quiz.models';
import { ConfirmDialogComponent } from '../../../shared/components/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-quiz-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
    TranslateModule
  ],
  template: `
    <div class="quiz-list-page">
      <div class="page-header">
        <div class="header-content">
          <h1>
            <mat-icon>quiz</mat-icon>
            {{ 'QUIZ.LIST_TITLE' | translate }}
          </h1>
          <p>Manage your quizzes and track your learning progress</p>
        </div>
        <button mat-raised-button color="primary" routerLink="/app/quizzes/new" class="create-btn">
          <mat-icon>add</mat-icon>
          {{ 'QUIZ.CREATE' | translate }}
        </button>
      </div>

      <div class="search-section">
        <mat-form-field appearance="outline" class="search-field">
          <mat-label>{{ 'COMMON.SEARCH' | translate }}</mat-label>
          <mat-icon matPrefix>search</mat-icon>
          <input matInput [formControl]="searchControl" placeholder="Search by quiz name...">
          @if (searchControl.value) {
            <button matSuffix mat-icon-button (click)="searchControl.setValue('')">
              <mat-icon>close</mat-icon>
            </button>
          }
        </mat-form-field>
        <div class="quiz-count">
          {{ filteredQuizzes().length }} quiz{{ filteredQuizzes().length !== 1 ? 'zes' : '' }}
        </div>
      </div>

      @if (isLoading()) {
        <div class="loading-container">
          <mat-spinner diameter="48"></mat-spinner>
          <p>Loading quizzes...</p>
        </div>
      } @else if (filteredQuizzes().length === 0 && !searchControl.value) {
        <div class="empty-state">
          <mat-icon>school</mat-icon>
          <h3>No quizzes yet</h3>
          <p>Create your first quiz from a YouTube video</p>
          <button mat-raised-button color="primary" routerLink="/app/quizzes/new">
            <mat-icon>add</mat-icon>
            Create Your First Quiz
          </button>
        </div>
      } @else if (filteredQuizzes().length === 0) {
        <div class="empty-state">
          <mat-icon>search_off</mat-icon>
          <h3>No results found</h3>
          <p>Try a different search term</p>
        </div>
      } @else {
        <div class="quiz-grid">
          @for (quiz of filteredQuizzes(); track quiz.id) {
            <div class="quiz-card">
              <div class="quiz-card-header">
                <div class="quiz-icon">
                  <mat-icon>quiz</mat-icon>
                </div>
                <div class="quiz-info">
                  <h3>{{ quiz.name }}</h3>
                  <span class="question-count">
                    <mat-icon>help_outline</mat-icon>
                    {{ quiz.questions_count }} questions
                  </span>
                </div>
              </div>
              <p class="quiz-description">{{ quiz.description || 'No description' }}</p>
              <div class="quiz-actions">
                <button mat-raised-button color="primary" [routerLink]="['/app/quizzes', quiz.id, 'run']">
                  <mat-icon>play_arrow</mat-icon>
                  Start
                </button>
                <button mat-stroked-button [routerLink]="['/app/quizzes', quiz.id, 'edit']">
                  <mat-icon>edit</mat-icon>
                  Edit
                </button>
                <button mat-icon-button color="warn" (click)="onDelete(quiz)" class="delete-btn">
                  <mat-icon>delete</mat-icon>
                </button>
              </div>
            </div>
          }
        </div>
      }
    </div>
  `,
  styles: [`
    .quiz-list-page {
      padding: var(--spacing-8);
      max-width: 1200px;
      margin: 0 auto;
      min-height: calc(100vh - 64px);
    }

    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: var(--spacing-8);
      padding-bottom: var(--spacing-6);
      border-bottom: 1px solid var(--color-divider);
    }

    .header-content h1 {
      display: flex;
      align-items: center;
      gap: var(--spacing-3);
      font-size: var(--font-size-h1);
      margin-bottom: var(--spacing-2);
    }

    .header-content h1 mat-icon {
      font-size: 32px;
      width: 32px;
      height: 32px;
      color: var(--color-primary);
    }

    .header-content p {
      color: var(--color-text-secondary);
      margin: 0;
    }

    .create-btn {
      padding: var(--spacing-3) var(--spacing-6) !important;
      border-radius: var(--radius-full) !important;
    }

    .search-section {
      display: flex;
      align-items: center;
      gap: var(--spacing-4);
      margin-bottom: var(--spacing-6);
    }

    .search-field {
      flex: 1;
      max-width: 400px;
    }

    .quiz-count {
      color: var(--color-text-secondary);
      font-size: var(--font-size-body2);
    }

    .loading-container {
      text-align: center;
      padding: var(--spacing-16);
    }

    .loading-container p {
      margin-top: var(--spacing-4);
      color: var(--color-text-secondary);
    }

    .empty-state {
      text-align: center;
      padding: var(--spacing-16) var(--spacing-6);
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
    }

    .empty-state mat-icon {
      font-size: 64px;
      width: 64px;
      height: 64px;
      color: var(--color-text-secondary);
      margin-bottom: var(--spacing-6);
    }

    .empty-state h3 {
      font-size: var(--font-size-h3);
      margin-bottom: var(--spacing-2);
      color: var(--color-text-primary);
    }

    .empty-state p {
      color: var(--color-text-secondary);
      margin-bottom: var(--spacing-6);
    }

    .quiz-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: var(--spacing-6);
    }

    .quiz-card {
      background: var(--color-surface);
      border-radius: var(--radius-lg);
      padding: var(--spacing-6);
      box-shadow: var(--shadow-sm);
      transition: transform var(--transition-normal), box-shadow var(--transition-normal);
    }

    .quiz-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-lg);
    }

    .quiz-card-header {
      display: flex;
      gap: var(--spacing-4);
      margin-bottom: var(--spacing-4);
    }

    .quiz-icon {
      width: 48px;
      height: 48px;
      background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .quiz-icon mat-icon {
      color: white;
    }

    .quiz-info {
      flex: 1;
      min-width: 0;
    }

    .quiz-info h3 {
      font-size: var(--font-size-h4);
      margin: 0 0 var(--spacing-1) 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .question-count {
      display: flex;
      align-items: center;
      gap: var(--spacing-1);
      color: var(--color-text-secondary);
      font-size: var(--font-size-caption);
    }

    .question-count mat-icon {
      font-size: 16px;
      width: 16px;
      height: 16px;
    }

    .quiz-description {
      color: var(--color-text-secondary);
      font-size: var(--font-size-body2);
      margin-bottom: var(--spacing-5);
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      min-height: 40px;
    }

    .quiz-actions {
      display: flex;
      gap: var(--spacing-2);
      align-items: center;
    }

    .quiz-actions button:first-child {
      flex: 1;
    }

    .delete-btn {
      margin-left: auto;
    }

    @media (max-width: 768px) {
      .page-header {
        flex-direction: column;
        gap: var(--spacing-4);
      }

      .search-section {
        flex-direction: column;
        align-items: stretch;
      }

      .search-field {
        max-width: none;
      }

      .quiz-grid {
        grid-template-columns: 1fr;
      }
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class QuizListComponent implements OnInit {
  private quizService = inject(QuizService);
  private notification = inject(NotificationService);
  private dialog = inject(MatDialog);
  private fb = inject(FormBuilder);

  isLoading = signal(false);
  quizzes = signal<QuizzDto[]>([]);
  searchControl = this.fb.control('');
  displayedColumns = ['name', 'description', 'questions_count', 'actions'];

  filteredQuizzes = signal<QuizzDto[]>([]);

  ngOnInit(): void {
    this.loadQuizzes();
    this.searchControl.valueChanges.subscribe(() => {
      this.filterQuizzes();
    });
  }

  loadQuizzes(): void {
    this.isLoading.set(true);
    this.quizService.getQuizzes().subscribe({
      next: (quizzes) => {
        this.quizzes.set(quizzes);
        this.filterQuizzes();
        this.isLoading.set(false);
      },
      error: () => {
        this.isLoading.set(false);
      }
    });
  }

  filterQuizzes(): void {
    const searchTerm = (this.searchControl.value || '').toLowerCase();
    const filtered = this.quizzes().filter(quiz =>
      quiz.name.toLowerCase().includes(searchTerm)
    );
    this.filteredQuizzes.set(filtered);
  }

  onDelete(quiz: QuizzDto): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'COMMON.CONFIRM_DELETE',
        message: 'COMMON.DELETE_CONFIRM_MESSAGE'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.quizService.deleteQuiz(quiz.id).subscribe({
          next: () => {
            this.notification.success('Quiz deleted');
            this.loadQuizzes();
          }
        });
      }
    });
  }
}
