import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'landing', pathMatch: 'full' },
  { path: 'landing', loadComponent: () => import('./features/landing/landing.component').then(m => m.LandingComponent) },

  // Auth (public)
  { path: 'auth/login', loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent) },
  { path: 'auth/register', loadComponent: () => import('./features/auth/register/register.component').then(m => m.RegisterComponent) },

  // App (protected)
  {
    path: 'app',
    canActivate: [authGuard],
    children: [
      { path: 'quizzes', loadComponent: () => import('./features/quizzes/quiz-list/quiz-list.component').then(m => m.QuizListComponent) },
      { path: 'quizzes/new', loadComponent: () => import('./features/quizzes/quiz-create/quiz-create.component').then(m => m.QuizCreateComponent) },
      { path: 'quizzes/:id/edit', loadComponent: () => import('./features/quizzes/quiz-edit/quiz-edit.component').then(m => m.QuizEditComponent) },
      { path: 'quizzes/:id/run', loadComponent: () => import('./features/run/run-start/run-start.component').then(m => m.RunStartComponent) },
      { path: 'quizzes/:id/run/q/:index', loadComponent: () => import('./features/run/question/question.component').then(m => m.QuestionComponent) },
      { path: 'quizzes/:id/run/feedback', loadComponent: () => import('./features/run/feedback/feedback.component').then(m => m.FeedbackComponent) },
      { path: 'quizzes/:id/run/results', loadComponent: () => import('./features/run/results/results.component').then(m => m.ResultsComponent) },
      { path: 'profile', loadComponent: () => import('./features/auth/profile/profile.component').then(m => m.ProfileComponent) },
    ]
  },

  { path: '**', redirectTo: 'landing' }
];
