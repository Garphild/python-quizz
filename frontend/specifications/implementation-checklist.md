# Frontend Implementation Checklist

> Декомпозиція специфікації на окремі задачі для імплементації Angular фронтенду

---

## Phase 1: Project Setup & Configuration

### 1.1 Ініціалізація проекту
- [x] Створити новий Angular проект (`ng new quiz-app --style=scss --routing`)
- [x] Налаштувати strict mode в `tsconfig.json`
- [x] Встановити Angular Material (`ng add @angular/material`)
- [x] Встановити @ngx-translate (`npm install @ngx-translate/core @ngx-translate/http-loader`)

### 1.2 Конфігурація середовища
- [x] Створити `proxy.conf.json` для API proxy
- [x] Налаштувати `environment.ts` з apiBasePath та мовами
- [x] Налаштувати `environment.prod.ts`
- [x] Додати proxy до `angular.json` (serve → proxyConfig)

### 1.3 Базова структура проекту
- [x] Створити папку `core/` (services, interceptors, guards, models)
- [x] Створити папку `features/` (auth, landing, quizzes, run)
- [x] Створити папку `shared/` (components, pipes)
- [x] Створити папку `persistence/` (IndexedDB repositories)

---

## Phase 2: Core Layer

### 2.1 Models (Types/Interfaces)
- [x] Створити `core/models/auth.models.ts` (LoginRequestDto, RegisterRequestDto, ProfileDto, etc.)
- [x] Створити `core/models/quiz.models.ts` (QuizzDto, QuestionDto, AnswerDto, etc.)
- [x] Створити `core/models/attempt.models.ts` (AttemptLocal, AttemptAnswerLocal, QuizStatsLocal)

### 2.2 Core Services
- [x] Створити `core/services/auth.service.ts`
  - [x] Реалізувати `currentUser` signal
  - [x] Реалізувати `isAuthenticated` computed
  - [x] Реалізувати `login()` method
  - [x] Реалізувати `register()` method
  - [x] Реалізувати `logout()` method
  - [x] Реалізувати `getProfile()` method
  - [x] Реалізувати `updateProfile()` method
  - [x] Реалізувати `changePassword()` method

- [x] Створити `core/services/quiz.service.ts`
  - [x] Реалізувати CRUD для quizzes
  - [x] Реалізувати CRUD для questions
  - [x] Реалізувати CRUD для answers
  - [x] Реалізувати `validateAnswer()` method

- [x] Створити `core/services/notification.service.ts`
  - [x] Реалізувати `success()` method
  - [x] Реалізувати `error()` method
  - [x] Реалізувати `info()` method

- [x] Створити `core/services/i18n.service.ts`
  - [x] Реалізувати `currentLang` signal
  - [x] Реалізувати `setLanguage()` method
  - [x] Реалізувати RTL support для Hebrew

### 2.3 Interceptors
- [x] Створити `core/interceptors/auth.interceptor.ts`
  - [x] Додати `withCredentials: true` для API запитів

- [x] Створити `core/interceptors/error.interceptor.ts`
  - [x] Обробка 401 → redirect на login
  - [x] Показ помилок через NotificationService

### 2.4 Guards
- [x] Створити `core/guards/auth.guard.ts`
  - [x] Перевірка `isAuthenticated()`
  - [x] Redirect на login з `returnUrl`

### 2.5 App Configuration
- [x] Налаштувати `app.config.ts`
  - [x] provideHttpClient з withInterceptors
  - [x] TranslateModule.forRoot
  - [x] provideRouter

- [x] Налаштувати `app.routes.ts`
  - [x] Public routes (landing, auth)
  - [x] Protected routes з authGuard

---

## Phase 3: Persistence Layer (IndexedDB)

### 3.1 IndexedDB Provider
- [x] Створити `persistence/indexed-db.provider.ts`
  - [x] Ініціалізація DB `quiz_app_db`
  - [x] Створення object stores (attempts, quiz_stats, app_state)
  - [x] Створення indexes

### 3.2 Repositories
- [x] Створити `persistence/attempt.repository.ts`
  - [x] `createAttempt()`
  - [x] `getAttempt()`
  - [x] `appendAnswer()`
  - [x] `finishAttempt()`
  - [x] `listAttemptsByQuiz()`
  - [x] `deleteAttempt()`

- [x] Створити `persistence/quiz-stats.repository.ts`
  - [x] `getStats()`
  - [x] `updateAfterAttempt()`

- [x] Створити `persistence/app-state.repository.ts`
  - [x] `setActiveAttempt()`
  - [x] `getActiveAttempt()`
  - [x] `clearActiveAttempt()`

---

## Phase 4: Shared Components

### 4.1 Header Component
- [x] Створити `shared/components/header/header.component.ts`
  - [x] Logo
  - [ ] Navigation links
  - [x] User menu (profile, logout)
  - [x] Language switch

### 4.2 Language Switch Component
- [x] Створити `shared/components/language-switch/language-switch.component.ts`
  - [x] Dropdown з мовами (uk, en, he)
  - [x] Зберігання вибору в localStorage

### 4.3 Confirm Dialog Component
- [x] Створити `shared/components/confirm-dialog/confirm-dialog.component.ts`
  - [x] Title, message
  - [x] Confirm/Cancel buttons

### 4.4 Loading Spinner Component
- [x] Створити `shared/components/loading-spinner/loading-spinner.component.ts`

### 4.5 Empty State Component
- [x] Створити `shared/components/empty-state/empty-state.component.ts`
  - [x] Icon, message, action button (optional)

---

## Phase 5: i18n (Translations)

### 5.1 Translation Files
- [x] Створити `assets/i18n/uk.json` (українська)
- [x] Створити `assets/i18n/en.json` (English)
- [x] Створити `assets/i18n/he.json` (עברית)

### 5.2 RTL Styles
- [x] Додати RTL styles в `styles.scss`

---

## Phase 6: Feature - Landing

### 6.1 Landing Component
- [x] Створити `features/landing/landing.component.ts`
  - [x] Hero section з описом продукту
  - [x] CTA buttons (Login, Register)
  - [x] Умовне відображення "Go to App" якщо authenticated
  - [ ] Responsive design (потребує покращення)

---

## Phase 7: Feature - Auth

### 7.1 Login Component
- [x] Створити `features/auth/login/login.component.ts`
  - [x] Reactive form (email, password)
  - [x] Валідація полів
  - [x] Submit → AuthService.login()
  - [x] Error handling та display
  - [x] Link to Register
  - [x] Redirect після успіху

### 7.2 Register Component
- [x] Створити `features/auth/register/register.component.ts`
  - [x] Reactive form (name, surname, email, password, confirmPassword)
  - [x] Валідація полів
  - [x] Валідація password === confirmPassword
  - [x] Submit → AuthService.register()
  - [x] Error handling
  - [x] Redirect на login після успіху

### 7.3 Profile Component
- [x] Створити `features/auth/profile/profile.component.ts`
  - [x] Display profile data
  - [x] Edit form (name, surname)
  - [x] Change password form
  - [x] Logout button

---

## Phase 8: Feature - Quizzes

### 8.1 Quiz List Component
- [x] Створити `features/quizzes/quiz-list/quiz-list.component.ts`
  - [x] Table з квізами (name, description, questions_count, created_at)
  - [x] Actions (Edit, Run, Delete)
  - [x] Search input (filter by name)
  - [x] Create button
  - [x] Loading state
  - [x] Empty state
  - [x] Delete confirmation dialog

### 8.2 Quiz Create Component
- [x] Створити `features/quizzes/quiz-create/quiz-create.component.ts`
  - [x] Form з YouTube URL input
  - [x] URL validation (YouTube pattern)
  - [x] Submit → QuizService.createQuiz()
  - [x] Loading state під час AI генерації
  - [x] Success → redirect на list

### 8.3 Quiz Edit Component
- [x] Створити `features/quizzes/quiz-edit/quiz-edit.component.ts`
  - [x] Load quiz data
  - [x] Edit name, description
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
  - [x] Save all changes
  - [x] Loading states
  - [ ] Confirmation dialogs для delete

---

## Phase 9: Feature - Quiz Run

### 9.1 Run Start Component
- [x] Створити `features/run/run-start/run-start.component.ts`
  - [x] Display quiz name, questions count
  - [x] Start button
  - [ ] Continue / Start New (якщо є незавершена спроба)
  - [x] Load quiz + questions
  - [x] Shuffle questions (Fisher-Yates)
  - [x] Create attempt в IndexedDB
  - [x] Navigate до першого питання

### 9.2 Question Component
- [x] Створити `features/run/question/question.component.ts`
  - [x] Display question text
  - [x] Radio group з відповідями
  - [x] Progress indicator (index / total)
  - [x] Submit button (disabled without selection)
  - [x] Submit → validateAnswer API
  - [x] Save answer → IndexedDB
  - [x] Navigate to feedback

### 9.3 Feedback Component
- [x] Створити `features/run/feedback/feedback.component.ts`
  - [x] Correct / Incorrect badge
  - [ ] Selected answer
  - [ ] Correct answer (якщо incorrect)
  - [ ] Explanation (description / valid_description)
  - [x] Next / Finish button
  - [x] Navigate to next question or results

### 9.4 Results Component
- [x] Створити `features/run/results/results.component.ts`
  - [x] Score display (count, percentage)
  - [ ] Questions summary list
  - [x] Finish attempt → IndexedDB
  - [x] Update stats → IndexedDB
  - [x] Retry button
  - [x] Back to list button

### 9.5 Run Service
- [ ] Створити `features/run/services/run.service.ts`
  - [ ] Current attempt state
  - [ ] Shuffle logic
  - [ ] Navigation helpers

---

## Phase 10: App Shell

### 10.1 App Component
- [x] Налаштувати `app.component.ts`
  - [x] Router outlet
  - [x] Header integration
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
