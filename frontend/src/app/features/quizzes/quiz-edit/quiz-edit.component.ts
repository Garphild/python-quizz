import { Component, inject, ChangeDetectionStrategy, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { TranslateModule } from '@ngx-translate/core';
import { QuizService } from '../../../core/services/quiz.service';
import { NotificationService } from '../../../core/services/notification.service';

@Component({
  selector: 'app-quiz-edit',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    TranslateModule
  ],
  template: `
    <div class="edit-container">
      <mat-card class="edit-card">
        <mat-card-header>
          <mat-card-title>{{ 'QUIZ.EDIT' | translate }}</mat-card-title>
        </mat-card-header>
        <mat-card-content>
          @if (isLoading()) {
            <mat-spinner></mat-spinner>
          } @else {
            <form [formGroup]="form" (ngSubmit)="onSubmit()">
              <mat-form-field appearance="fill" class="full-width">
                <mat-label>{{ 'QUIZ.NAME' | translate }}</mat-label>
                <input matInput formControlName="name" required>
              </mat-form-field>

              <mat-form-field appearance="fill" class="full-width">
                <mat-label>{{ 'QUIZ.DESCRIPTION' | translate }}</mat-label>
                <textarea matInput formControlName="description" rows="4"></textarea>
              </mat-form-field>

              <div class="button-group">
                <button mat-raised-button color="primary" type="submit" [disabled]="form.invalid || isSaving()">
                  {{ 'COMMON.SAVE' | translate }}
                </button>
              </div>
            </form>
          }
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [`
    .edit-container {
      padding: 20px;
      max-width: 600px;
      margin: 0 auto;
    }

    .full-width {
      width: 100%;
      margin-bottom: 20px;
    }

    .button-group {
      display: flex;
      gap: 10px;
      margin-top: 20px;
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class QuizEditComponent implements OnInit {
  private quizService = inject(QuizService);
  private notification = inject(NotificationService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private fb = inject(FormBuilder);

  isLoading = signal(false);
  isSaving = signal(false);
  quizId = 0;
  form = this.fb.group({
    name: ['', Validators.required],
    description: ['']
  });

  ngOnInit(): void {
    this.quizId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadQuiz();
  }

  loadQuiz(): void {
    this.isLoading.set(true);
    this.quizService.getQuiz(this.quizId).subscribe({
      next: (quiz) => {
        this.form.patchValue({
          name: quiz.name,
          description: quiz.description
        });
        this.isLoading.set(false);
      },
      error: () => {
        this.isLoading.set(false);
      }
    });
  }

  onSubmit(): void {
    if (this.form.invalid) {
      return;
    }

    this.isSaving.set(true);
    const data = this.form.getRawValue() as any;

    this.quizService.updateQuiz(this.quizId, data).subscribe({
      next: () => {
        this.notification.success('Quiz updated');
        this.router.navigate(['/app/quizzes']);
      },
      error: () => {
        this.isSaving.set(false);
      }
    });
  }
}
