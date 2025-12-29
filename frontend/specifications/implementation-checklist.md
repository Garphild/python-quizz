# Frontend Implementation Checklist

> Декомпозиція специфікації на окремі задачі для імплементації Angular фронтенду

---

## Phase 1: Project Setup & Configuration

### 1.1 Ініціалізація проекту
- [ ] Створити новий Angular проект (`ng new quiz-app --style=scss --routing`)
- [ ] Налаштувати strict mode в `tsconfig.json`
- [ ] Встановити Angular Material (`ng add @angular/material`)
- [ ] Встановити @ngx-translate (`npm install @ngx-translate/core @ngx-translate/http-loader`)

### 1.2 Конфігурація середовища
- [ ] Створити `proxy.conf.json` для API proxy
- [ ] Налаштувати `environment.ts` з apiBasePath та мовами
- [ ] Налаштувати `environment.prod.ts`
- [ ] Додати proxy до `angular.json` (serve → proxyConfig)

### 1.3 Базова структура проекту
- [ ] Створити папку `core/` (services, interceptors, guards, models)
- [ ] Створити папку `features/` (auth, landing, quizzes, run)
- [ ] Створити папку `shared/` (components, pipes)
- [ ] Створити папку `persistence/` (IndexedDB repositories)

---

## Phase 2: Core Layer

### 2.1 Models (Types/Interfaces)
- [ ] Створити `core/models/auth.models.ts` (LoginRequestDto, RegisterRequestDto, ProfileDto, etc.)
- [ ] Створити `core/models/quiz.models.ts` (QuizzDto, QuestionDto, AnswerDto, etc.)
- [ ] Створити `core/models/attempt.models.ts` (AttemptLocal, AttemptAnswerLocal, QuizStatsLocal)

### 2.2 Core Services
- [ ] Створити `core/services/auth.service.ts`
  - [ ] Реалізувати `currentUser` signal
  - [ ] Реалізувати `isAuthenticated` computed
  - [ ] Реалізувати `login()` method
  - [ ] Реалізувати `register()` method
  - [ ] Реалізувати `logout()` method
  - [ ] Реалізувати `getProfile()` method
  - [ ] Реалізувати `updateProfile()` method
  - [ ] Реалізувати `changePassword()` method

- [ ] Створити `core/services/quiz.service.ts`
  - [ ] Реалізувати CRUD для quizzes
  - [ ] Реалізувати CRUD для questions
  - [ ] Реалізувати CRUD для answers
  - [ ] Реалізувати `validateAnswer()` method

- [ ] Створити `core/services/notification.service.ts`
  - [ ] Реалізувати `success()` method
  - [ ] Реалізувати `error()` method
  - [ ] Реалізувати `info()` method

- [ ] Створити `core/services/i18n.service.ts`
  - [ ] Реалізувати `currentLang` signal
  - [ ] Реалізувати `setLanguage()` method
  - [ ] Реалізувати RTL support для Hebrew

### 2.3 Interceptors
- [ ] Створити `core/interceptors/auth.interceptor.ts`
  - [ ] Додати `withCredentials: true` для API запитів

- [ ] Створити `core/interceptors/error.interceptor.ts`
  - [ ] Обробка 401 → redirect на login
  - [ ] Показ помилок через NotificationService

### 2.4 Guards
- [ ] Створити `core/guards/auth.guard.ts`
  - [ ] Перевірка `isAuthenticated()`
  - [ ] Redirect на login з `returnUrl`

### 2.5 App Configuration
- [ ] Налаштувати `app.config.ts`
  - [ ] provideHttpClient з withInterceptors
  - [ ] TranslateModule.forRoot
  - [ ] provideRouter

- [ ] Налаштувати `app.routes.ts`
  - [ ] Public routes (landing, auth)
  - [ ] Protected routes з authGuard

---

## Phase 3: Persistence Layer (IndexedDB)

### 3.1 IndexedDB Provider
- [ ] Створити `persistence/indexed-db.provider.ts`
  - [ ] Ініціалізація DB `quiz_app_db`
  - [ ] Створення object stores (attempts, quiz_stats, app_state)
  - [ ] Створення indexes

### 3.2 Repositories
- [ ] Створити `persistence/attempt.repository.ts`
  - [ ] `createAttempt()`
  - [ ] `getAttempt()`
  - [ ] `appendAnswer()`
  - [ ] `finishAttempt()`
  - [ ] `listAttemptsByQuiz()`
  - [ ] `deleteAttempt()`

- [ ] Створити `persistence/quiz-stats.repository.ts`
  - [ ] `getStats()`
  - [ ] `updateAfterAttempt()`

- [ ] Створити `persistence/app-state.repository.ts`
  - [ ] `setActiveAttempt()`
  - [ ] `getActiveAttempt()`
  - [ ] `clearActiveAttempt()`

---

## Phase 4: Shared Components

### 4.1 Header Component
- [ ] Створити `shared/components/header/header.component.ts`
  - [ ] Logo
  - [ ] Navigation links
  - [ ] User menu (profile, logout)
  - [ ] Language switch

### 4.2 Language Switch Component
- [ ] Створити `shared/components/language-switch/language-switch.component.ts`
  - [ ] Dropdown з мовами (uk, en, he)
  - [ ] Зберігання вибору в localStorage

### 4.3 Confirm Dialog Component
- [ ] Створити `shared/components/confirm-dialog/confirm-dialog.component.ts`
  - [ ] Title, message
  - [ ] Confirm/Cancel buttons

### 4.4 Loading Spinner Component
- [ ] Створити `shared/components/loading-spinner/loading-spinner.component.ts`

### 4.5 Empty State Component
- [ ] Створити `shared/components/empty-state/empty-state.component.ts`
  - [ ] Icon, message, action button (optional)

---

## Phase 5: i18n (Translations)

### 5.1 Translation Files
- [ ] Створити `assets/i18n/uk.json` (українська)
- [ ] Створити `assets/i18n/en.json` (English)
- [ ] Створити `assets/i18n/he.json` (עברית)

### 5.2 RTL Styles
- [ ] Додати RTL styles в `styles.scss`

---

## Phase 6: Feature - Landing

### 6.1 Landing Component
- [ ] Створити `features/landing/landing.component.ts`
  - [ ] Hero section з описом продукту
  - [ ] CTA buttons (Login, Register)
  - [ ] Умовне відображення "Go to App" якщо authenticated
  - [ ] Responsive design

---

## Phase 7: Feature - Auth

### 7.1 Login Component
- [ ] Створити `features/auth/login/login.component.ts`
  - [ ] Reactive form (email, password)
  - [ ] Валідація полів
  - [ ] Submit → AuthService.login()
  - [ ] Error handling та display
  - [ ] Link to Register
  - [ ] Redirect після успіху

### 7.2 Register Component
- [ ] Створити `features/auth/register/register.component.ts`
  - [ ] Reactive form (name, surname, email, password, confirmPassword)
  - [ ] Валідація полів
  - [ ] Валідація password === confirmPassword
  - [ ] Submit → AuthService.register()
  - [ ] Error handling
  - [ ] Redirect на login після успіху

### 7.3 Profile Component
- [ ] Створити `features/auth/profile/profile.component.ts`
  - [ ] Display profile data
  - [ ] Edit form (name, surname)
  - [ ] Change password form
  - [ ] Logout button

---

## Phase 8: Feature - Quizzes

### 8.1 Quiz List Component
- [ ] Створити `features/quizzes/quiz-list/quiz-list.component.ts`
  - [ ] Table з квізами (name, description, questions_count, created_at)
  - [ ] Actions (Edit, Run, Delete)
  - [ ] Search input (filter by name)
  - [ ] Create button
  - [ ] Loading state
  - [ ] Empty state
  - [ ] Delete confirmation dialog

### 8.2 Quiz Create Component
- [ ] Створити `features/quizzes/quiz-create/quiz-create.component.ts`
  - [ ] Form з YouTube URL input
  - [ ] URL validation (YouTube pattern)
  - [ ] Submit → QuizService.createQuiz()
  - [ ] Loading state під час AI генерації
  - [ ] Success → redirect на list

### 8.3 Quiz Edit Component
- [ ] Створити `features/quizzes/quiz-edit/quiz-edit.component.ts`
  - [ ] Load quiz data
  - [ ] Edit name, description
  - [ ] Questions list (accordion/cards)
    - [ ] Edit question text
    - [ ] Delete question
    - [ ] Add question
  - [ ] Answers list per question
    - [ ] Edit answer text
    - [ ] Mark as correct
    - [ ] Edit description/valid_description
    - [ ] Delete answer
    - [ ] Add answer
  - [ ] Save all changes
  - [ ] Loading states
  - [ ] Confirmation dialogs для delete

---

## Phase 9: Feature - Quiz Run

### 9.1 Run Start Component
- [ ] Створити `features/run/run-start/run-start.component.ts`
  - [ ] Display quiz name, questions count
  - [ ] Start button
  - [ ] Continue / Start New (якщо є незавершена спроба)
  - [ ] Load quiz + questions
  - [ ] Shuffle questions (Fisher-Yates)
  - [ ] Create attempt в IndexedDB
  - [ ] Navigate до першого питання

### 9.2 Question Component
- [ ] Створити `features/run/question/question.component.ts`
  - [ ] Display question text
  - [ ] Radio group з відповідями
  - [ ] Progress indicator (index / total)
  - [ ] Submit button (disabled without selection)
  - [ ] Submit → validateAnswer API
  - [ ] Save answer → IndexedDB
  - [ ] Navigate to feedback

### 9.3 Feedback Component
- [ ] Створити `features/run/feedback/feedback.component.ts`
  - [ ] Correct / Incorrect badge
  - [ ] Selected answer
  - [ ] Correct answer (якщо incorrect)
  - [ ] Explanation (description / valid_description)
  - [ ] Next / Finish button
  - [ ] Navigate to next question or results

### 9.4 Results Component
- [ ] Створити `features/run/results/results.component.ts`
  - [ ] Score display (count, percentage)
  - [ ] Questions summary list
  - [ ] Finish attempt → IndexedDB
  - [ ] Update stats → IndexedDB
  - [ ] Retry button
  - [ ] Back to list button

### 9.5 Run Service
- [ ] Створити `features/run/services/run.service.ts`
  - [ ] Current attempt state
  - [ ] Shuffle logic
  - [ ] Navigation helpers

---

## Phase 10: App Shell

### 10.1 App Component
- [ ] Налаштувати `app.component.ts`
  - [ ] Router outlet
  - [ ] Header integration
  - [ ] Global error handling

---

## Phase 11: Testing & QA

### 11.1 Unit Tests
- [ ] Tests для AuthService
- [ ] Tests для QuizService
- [ ] Tests для IndexedDB repositories
- [ ] Tests для Guards
- [ ] Tests для Interceptors

### 11.2 E2E Tests
- [ ] Auth flow (register, login, logout)
- [ ] Quiz CRUD
- [ ] Quiz run flow

### 11.3 Accessibility
- [ ] WCAG AA compliance check
- [ ] Focus management
- [ ] ARIA attributes
- [ ] Color contrast

---

## Phase 12: Final Polish

### 12.1 Performance
- [ ] Lazy loading для feature routes
- [ ] OnPush change detection
- [ ] trackBy для @for loops

### 12.2 Error Handling
- [ ] Global error handler
- [ ] User-friendly error messages

### 12.3 Documentation
- [ ] README з інструкціями запуску
- [ ] API documentation

---

## Summary

| Phase | Tasks | Priority |
|-------|-------|----------|
| 1. Setup | 12 | 🔴 Critical |
| 2. Core | 26 | 🔴 Critical |
| 3. Persistence | 12 | 🔴 Critical |
| 4. Shared | 5 | 🟡 High |
| 5. i18n | 4 | 🟡 High |
| 6. Landing | 1 | 🟢 Medium |
| 7. Auth | 3 | 🔴 Critical |
| 8. Quizzes | 3 | 🔴 Critical |
| 9. Run | 5 | 🔴 Critical |
| 10. App Shell | 1 | 🟢 Medium |
| 11. Testing | 7 | 🟡 High |
| 12. Polish | 4 | 🟢 Medium |

**Total: ~83 tasks**

---

## Recommended Order

1. **Phase 1** → Setup
2. **Phase 2.1-2.2** → Models + Auth/Quiz Services
3. **Phase 2.3-2.5** → Interceptors, Guards, Config
4. **Phase 7.1-7.2** → Login + Register
5. **Phase 6** → Landing
6. **Phase 8.1** → Quiz List
7. **Phase 8.2-8.3** → Quiz Create + Edit
8. **Phase 3** → IndexedDB
9. **Phase 9** → Quiz Run
10. **Phase 4-5** → Shared + i18n
11. **Phase 7.3** → Profile
12. **Phase 11-12** → Testing + Polish
