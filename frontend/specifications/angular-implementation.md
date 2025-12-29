# Angular Frontend Implementation Specification

> Специфікація для імплементації фронтенду на Angular для додатку "Quiz"

---

# 1) Мета і межі

## Мета

Створити SPA на Angular, де користувач:

- Реєструється / логіниться / виходить
- Бачить лендінг із CTA
- Керує власними квізами (list / search / filter / create / edit / delete)
- Проходить квіз (питання в випадковому порядку, серверна валідація, feedback, фінальні результати)
- Має локально збережену історію спроб і статистику (IndexedDB)

## Межі

- **Тільки фронтенд**
- Бекенд доступний на `localhost:8000` через proxy
- Контракт API адаптується в одному місці (ApiClient + типи)

---

# 2) Технологічні вимоги

| Технологія | Версія/Деталі                             |
| -------------------- | ----------------------------------------------------- |
| Angular              | ≥ 17 (standalone components, signals)                |
| Router               | + Guards                                              |
| HttpClient           | + Interceptors                                        |
| Forms                | Reactive Forms                                        |
| RxJS                 | Для async операцій                         |
| UI Kit               | Angular Material (рекомендовано)         |
| i18n                 | uk / en / he (RTL для Hebrew)                      |
| Persistence          | IndexedDB через wrapper + репозиторії |

### Angular Best Practices

- Standalone components (без NgModules)
- Signals для state management
- `input()` / `output()` замість декораторів
- `computed()` для derived state
- `ChangeDetectionStrategy.OnPush`
- Native control flow (`@if`, `@for`, `@switch`)
- `inject()` замість constructor injection

---

# 3) Конфігурація середовища

## 3.1 Proxy

**proxy.conf.json:**

```json
{
  "/api": {
    "target": "http://localhost:8000",
    "changeOrigin": true,
    "secure": false
  }
}
```

## 3.2 Environment

**environment.ts:**

```typescript
export const environment = {
  production: false,
  apiBasePath: '/api',
  defaultLanguage: 'uk',
  supportedLanguages: ['uk', 'en', 'he']
};
```

---

# 4) API Endpoints (Backend Contract)

## 4.1 Authentication

| Method | Endpoint                  | Request                                 | Response       | Notes                          |
| ------ | ------------------------- | --------------------------------------- | -------------- | ------------------------------ |
| POST   | `/api/auth/register`      | `{ email, password, name, surname? }`   | `boolean`      | `true` при успехе              |
| POST   | `/api/auth/login`         | `{ email, password }`                   | `ProfileDto`   | Token в cookie `auth_token`    |
| POST   | `/api/auth/logout`        | —                                       | `boolean`      | Видаляє cookie                 |
| GET    | `/api/auth/profile`       | —                                       | `ProfileDto`   | Потребує auth cookie           |
| POST   | `/api/auth/change-password` | `{ old_password, new_password }`      | `ProfileDto`   | Зміна пароля                   |
| POST   | `/api/auth/update-profile`  | `{ name?, surname? }`                 | `ProfileDto`   | Оновлення профілю              |

**Note:** Токен JWT встановлюється як HttpOnly cookie `auth_token`, а не в response body.

## 4.2 Quizzes (Public)

| Method | Endpoint                  | Request                     | Response      |
| ------ | ------------------------- | --------------------------- | ------------- |
| GET    | `/api/quizz`              | —                           | `QuizzDto[]`  |
| GET    | `/api/quizz/:id`          | —                           | `QuizzDto`    |
| POST   | `/api/quizz`              | `{ url }`                   | `QuizzDto`    |
| PUT    | `/api/quizz/:id`          | `{ name?, description? }`   | `QuizzDto`    |
| DELETE | `/api/quizz/:id`          | —                           | `boolean`     |

**Note:** `CreateQuizzDto` принимает только `url` (YouTube URL). Квиз создается с автоматической генерацией вопросов через AI.

## 4.3 Questions

| Method | Endpoint                                | Request      | Response          |
| ------ | --------------------------------------- | ------------ | ----------------- |
| GET    | `/api/quizz/:quizzId/questions`         | —            | `QuestionDto[]`   |
| GET    | `/api/quizz/:quizzId/questions/:id`     | —            | `QuestionDto`     |
| POST   | `/api/quizz/:quizzId/questions`         | `{ text }`   | `QuestionDto`     |
| PUT    | `/api/quizz/:quizzId/questions/:id`     | `{ text }`   | `QuestionDto`     |
| DELETE | `/api/quizz/:quizzId/questions/:id`     | —            | `boolean`         |

## 4.4 Answers

| Method | Endpoint                                          | Request                                                    | Response           |
| ------ | ------------------------------------------------- | ---------------------------------------------------------- | ------------------ |
| GET    | `/api/quizz/:quizzId/answers`                     | —                                                          | `AnswerDto[]`      |
| GET    | `/api/quizz/:quizzId/answers/:id`                 | —                                                          | `AnswerDto`        |
| POST   | `/api/quizz/:quizzId/answers`                     | `{ text, is_correct, description, valid_description? }`   | `AnswerDto`        |
| PUT    | `/api/quizz/:quizzId/answers/:id`                 | `{ text, is_correct, description, valid_description? }`    | `AnswerDto`        |
| DELETE | `/api/quizz/:quizzId/answers/:id`                 | —                                                          | `boolean`          |
| GET    | `/api/quizz/:quizzId/answers/validate/:questionId/:answerId` | —                                                  | `ValidateAnswerDto` |

**Note:** Endpoint валидации возвращает `is_correct`, `description` и `valid_description` для feedback.

---

# 5) Дані та моделі (Frontend Types)

## 5.1 Auth Types

```typescript
// Request DTOs
interface LoginRequestDto {
  email: string;
  password: string;
}

interface RegisterRequestDto {
  email: string;
  password: string;
  name: string;
  surname?: string;
}

interface UpdateProfileDto {
  name?: string;
  surname?: string;
}

interface ChangePasswordDto {
  old_password: string;
  new_password: string;
}

// Response DTOs
interface ProfileDto {
  id: number;
  email: string;
  name: string;
  surname?: string;
}
```

## 5.2 Quiz Types

```typescript
interface QuizzDto {
  id: number;
  name: string;
  description: string;
  url: string; // YouTube URL
  questions_count: number;
  created_at?: string;
  updated_at?: string;
  deleted_at?: string;
}

interface CreateQuizzDto {
  url: string; // YouTube URL - AI генерирует вопросы из видео
}

interface UpdateQuizzDto {
  name?: string;
  description?: string;
}
```

## 5.3 Question Types

```typescript
interface QuestionDto {
  id: number;
  text: string;
  quizz_id: number; // Зв'язок з квізом
  created_at: string;
  updated_at: string;
  deleted_at?: string;
}

interface CreateQuestionDto {
  text: string;
}

interface UpdateQuestionDto {
  text: string;
}

interface QuestionListDto {
  questions: QuestionDto[];
}
```

## 5.4 Answer Types

```typescript
interface AnswerDto {
  id: number;
  text: string;
  is_correct: boolean;
  question_id: number; // Зв'язок з питанням (ВАЖЛИВО: потрібно додати на бекенді!)
  description: string; // Пояснення чому відповідь неправильна
  valid_description?: string; // Пояснення чому відповідь правильна
}

interface CreateAnswerDto {
  text: string;
  is_correct: boolean;
  description: string;
  valid_description?: string;
}

interface UpdateAnswerDto {
  text: string; // required
  is_correct: boolean; // required
  description: string; // required
  valid_description?: string;
}

interface ValidateAnswerDto {
  is_correct: boolean;
  description: string;
  valid_description?: string;
}
```

## 5.5 Local Attempt Types (IndexedDB)

```typescript
interface AttemptLocal {
  attemptId: string; // UUID
  quizId: number;
  startedAt: number;
  finishedAt?: number;
  questionOrder: number[]; // shuffled question IDs
  answers: AttemptAnswerLocal[];
  score?: number;
  total?: number;
}

interface AttemptAnswerLocal {
  questionId: number;
  selectedOptionId: number;
  isCorrect: boolean;
  correctOptionId?: number;
  explanation?: string;
}

interface QuizStatsLocal {
  quizId: number;
  attemptsCount: number;
  bestScore: number;
  lastScore: number;
  lastAttemptAt: number;
}
```

---

# 6) IndexedDB Persistence

## 6.1 Database

- **DB name:** `quiz_app_db`
- **Version:** 1

## 6.2 Object Stores

### `attempts`

- keyPath: `attemptId`
- indexes:
  - `by_quizId` (quizId)
  - `by_startedAt` (startedAt)

### `quiz_stats`

- keyPath: `quizId`
- indexes:
  - `by_lastAttemptAt` (lastAttemptAt)

### `app_state`

- keyPath: `key`
- records:
  - `activeAttempt:<quizId>` → `attemptId`

## 6.3 Repositories

### AttemptRepository

```typescript
interface AttemptRepository {
  createAttempt(quizId: number, questionOrder: number[]): Promise<string>;
  getAttempt(attemptId: string): Promise<AttemptLocal | null>;
  appendAnswer(attemptId: string, answer: AttemptAnswerLocal): Promise<void>;
  finishAttempt(attemptId: string, score: number, total: number): Promise<void>;
  listAttemptsByQuiz(quizId: number, limit?: number): Promise<AttemptLocal[]>;
  deleteAttempt(attemptId: string): Promise<void>;
}
```

### QuizStatsRepository

```typescript
interface QuizStatsRepository {
  getStats(quizId: number): Promise<QuizStatsLocal | null>;
  updateAfterAttempt(quizId: number, score: number): Promise<QuizStatsLocal>;
}
```

### AppStateRepository

```typescript
interface AppStateRepository {
  setActiveAttempt(quizId: number, attemptId: string): Promise<void>;
  getActiveAttempt(quizId: number): Promise<string | null>;
  clearActiveAttempt(quizId: number): Promise<void>;
}
```

---

# 7) Структура проєкту

```
src/
├── app/
│   ├── core/
│   │   ├── services/
│   │   │   ├── api.service.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── notification.service.ts
│   │   │   └── i18n.service.ts
│   │   ├── interceptors/
│   │   │   └── auth.interceptor.ts
│   │   ├── guards/
│   │   │   └── auth.guard.ts
│   │   └── models/
│   │       ├── auth.models.ts
│   │       ├── quiz.models.ts
│   │       └── attempt.models.ts
│   │
│   ├── features/
│   │   ├── auth/
│   │   │   ├── login/
│   │   │   │   └── login.component.ts
│   │   │   └── register/
│   │   │       └── register.component.ts
│   │   │
│   │   ├── landing/
│   │   │   └── landing.component.ts
│   │   │
│   │   ├── quizzes/
│   │   │   ├── quiz-list/
│   │   │   │   └── quiz-list.component.ts
│   │   │   ├── quiz-create/
│   │   │   │   └── quiz-create.component.ts
│   │   │   ├── quiz-edit/
│   │   │   │   └── quiz-edit.component.ts
│   │   │   └── services/
│   │   │       └── quiz.service.ts
│   │   │
│   │   └── run/
│   │       ├── run-start/
│   │       │   └── run-start.component.ts
│   │       ├── question/
│   │       │   └── question.component.ts
│   │       ├── feedback/
│   │       │   └── feedback.component.ts
│   │       ├── results/
│   │       │   └── results.component.ts
│   │       └── services/
│   │           └── run.service.ts
│   │
│   ├── persistence/
│   │   ├── indexed-db.provider.ts
│   │   ├── attempt.repository.ts
│   │   ├── quiz-stats.repository.ts
│   │   └── app-state.repository.ts
│   │
│   ├── shared/
│   │   ├── components/
│   │   │   ├── header/
│   │   │   │   └── header.component.ts
│   │   │   └── language-switch/
│   │   │       └── language-switch.component.ts
│   │   └── pipes/
│   │
│   ├── app.component.ts
│   ├── app.config.ts
│   └── app.routes.ts
│
├── assets/
│   └── i18n/
│       ├── uk.json
│       ├── en.json
│       └── he.json
│
└── environments/
    ├── environment.ts
    └── environment.prod.ts
```

---

# 8) Routing

```typescript
export const routes: Routes = [
  { path: '', component: LandingComponent },
  
  // Auth (public)
  { path: 'auth/login', component: LoginComponent },
  { path: 'auth/register', component: RegisterComponent },
  
  // App (protected)
  {
    path: 'app',
    canActivate: [authGuard],
    children: [
      { path: 'quizzes', component: QuizListComponent },
      { path: 'quizzes/new', component: QuizCreateComponent },
      { path: 'quizzes/:id/edit', component: QuizEditComponent },
      { path: 'quizzes/:id/run', component: RunStartComponent },
      { path: 'quizzes/:id/run/q/:index', component: QuestionComponent },
      { path: 'quizzes/:id/run/feedback', component: FeedbackComponent },
      { path: 'quizzes/:id/run/results', component: ResultsComponent },
      { path: 'profile', component: ProfileComponent },
    ]
  },
  
  { path: '**', redirectTo: '' }
];
```

---

# 9) Екрани та поведінка

## 9.1 Landing (`/`)

**UI:**

- Пояснення продукту
- Кнопки: Login, Register
- Якщо authenticated: "Go to App"

**Acceptance:**

- [ ] Кнопки ведуть на правильні маршрути
- [ ] Мова перемикається і зберігається

---

## 9.2 Login (`/auth/login`)

**UI:**

- email (input)
- password (input)
- Submit button
- Error message area
- Link to Register

**Логіка:**

- POST `/api/auth/login`
- Сервер встановлює `auth_token` cookie (HttpOnly)
- Зберегти `ProfileDto` в `AuthService.currentUser` signal
- Redirect до `/app/quizzes`

**Acceptance:**

- [ ] Невірні креденшали → показати помилку "Invalid credentials"
- [ ] Успішно → redirect + доступ до приватних сторінок

---

## 9.3 Register (`/auth/register`)

**UI:**

- name (input)
- surname (input, optional)
- email (input)
- password (input)
- confirmPassword (input)
- Submit button

**Логіка:**

- Валідація confirmPassword === password
- POST `/api/auth/register`
- Response: `boolean` (true при успіху)
- Після успіху → redirect на login

**Acceptance:**

- [ ] Валідація confirmPassword
- [ ] Існуючий email → помилка "User with this email already exists" (400)
- [ ] Успіх → redirect на login

---

## 9.4 Quiz List (`/app/quizzes`)

**UI:**

- Таблиця:
  - Name
  - Description
  - Questions Count
  - Created At
  - Actions: Edit / Run / Delete
- Search input (по name)
- Create button (веде на форму з YouTube URL)

**Логіка:**

- GET `/api/quizz`
- Client-side filtering по name
- Pagination (якщо потрібна)

**Acceptance:**

- [ ] Пошук працює
- [ ] Create веде на форму з URL input
- [ ] Edit/Run/Delete працюють

---

## 9.5 Create Quiz (`/app/quizzes/new`)

**UI:**

- YouTube URL (input, required)
- Submit button
- Loading state під час генерації вопросів AI

**Логіка:**

- POST `/api/quizz` з `{ url }`
- AI генерирует вопросы и ответы автоматически
- Redirect на список після успіху

**Acceptance:**

- [ ] Валідація YouTube URL
- [ ] Успіх → snackbar + redirect
- [ ] Loading state під час обробки

---

## 9.6 Edit Quiz (`/app/quizzes/:id/edit`)

**UI:**

- Заголовок: name (можна редагувати)
- Description (можна редагувати)
- Список питань (cards/accordion):
  - Question text (input)
  - Answers list:
    - answer text
    - is_correct (radio/checkbox)
    - description (пояснення неправильної відповіді)
    - valid_description (пояснення правильної відповіді)
    - delete answer
  - Add answer
  - Delete question
- Add question
- Save button

**Логіка:**

- GET `/api/quizz/:id` + GET `/api/quizz/:id/questions` + GET `/api/quizz/:id/answers`
- PUT `/api/quizz/:id` для оновлення name/description
- POST/PUT/DELETE для питань і відповідей

**Acceptance:**

- [ ] Можна редагувати питання/відповіді
- [ ] Можна додавати/видаляти
- [ ] Save працює
- [ ] Пояснення (description/valid_description) зберігаються

---

## 9.7 Run Start (`/app/quizzes/:id/run`)

**UI:**

- Назва квіза
- Кількість питань
- Start button
- Continue / Start New (якщо є незавершена спроба)

**Логіка:**

- GET quiz detail
- Generate UUID для attemptId
- Shuffle questions (Fisher–Yates)
- Зберегти в IndexedDB
- Redirect до першого питання

**Acceptance:**

- [ ] Порядок питань стабільний для спроби

---

## 9.8 Question (`/app/quizzes/:id/run/q/:index`)

**UI:**

- Question text
- Radio group з варіантами
- Submit button
- Progress: `index+1 / total`

**Логіка:**

- Взяти attempt з IndexedDB
- Після submit → валідація на бекенді
- Зберегти результат → feedback

**Acceptance:**

- [ ] Без вибору — submit disabled
- [ ] Після submit — lock UI

---

## 9.9 Feedback (`/app/quizzes/:id/run/feedback`)

**UI:**

- Correct / Incorrect badge
- Selected answer
- Correct answer (якщо incorrect)
- Explanation (якщо є)
- Next / Finish button

**Логіка:**

- Next → наступне питання
- Finish → results

---

## 9.10 Results (`/app/quizzes/:id/run/results`)

**UI:**

- Score, %
- Список питань з відповідями
- Retry / Back to list buttons

**Логіка:**

- Обчислити score
- `finishAttempt` в IndexedDB
- `updateAfterAttempt` для stats

---

## 9.11 Profile (`/app/profile`)

**UI:**

- Дані профілю (email, name, surname)
- Форма редагування (name, surname)
- Секція зміни пароля (old_password, new_password, confirm_password)
- Save buttons

**Логіка:**

- GET `/api/auth/profile` при завантаженні
- POST `/api/auth/update-profile` для оновлення даних
- POST `/api/auth/change-password` для зміни пароля
- Logout button → POST `/api/auth/logout` → redirect на `/`

**Acceptance:**

- [ ] Профіль відображається коректно
- [ ] Можна змінити name/surname
- [ ] Можна змінити пароль
- [ ] Logout очищає session і редіректить

---

# 10) Core Services

## AuthService

```typescript
@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  
  currentUser = signal<ProfileDto | null>(null);
  isAuthenticated = computed(() => !!this.currentUser());
  
  // Auth endpoints (cookie-based)
  login(credentials: LoginRequestDto): Observable<ProfileDto>;
  register(data: RegisterRequestDto): Observable<boolean>;
  logout(): Observable<boolean>;
  
  // Profile endpoints
  getProfile(): Observable<ProfileDto>;
  updateProfile(data: UpdateProfileDto): Observable<ProfileDto>;
  changePassword(data: ChangePasswordDto): Observable<ProfileDto>;
  
  // Note: Token управляется через HttpOnly cookie, не через localStorage
}
```

## QuizService

```typescript
@Injectable({ providedIn: 'root' })
export class QuizService {
  private http = inject(HttpClient);
  
  // Quizzes
  getQuizzes(): Observable<QuizzDto[]>;
  getQuiz(id: number): Observable<QuizzDto>;
  createQuiz(data: CreateQuizzDto): Observable<QuizzDto>;
  updateQuiz(id: number, data: UpdateQuizzDto): Observable<QuizzDto>;
  deleteQuiz(id: number): Observable<boolean>;
  
  // Questions
  getQuestions(quizId: number): Observable<QuestionDto[]>;
  getQuestion(quizId: number, questionId: number): Observable<QuestionDto>;
  createQuestion(quizId: number, data: CreateQuestionDto): Observable<QuestionDto>;
  updateQuestion(quizId: number, questionId: number, data: UpdateQuestionDto): Observable<QuestionDto>;
  deleteQuestion(quizId: number, questionId: number): Observable<boolean>;
  
  // Answers
  getAnswers(quizId: number): Observable<AnswerDto[]>;
  getAnswer(quizId: number, answerId: number): Observable<AnswerDto>;
  createAnswer(quizId: number, data: CreateAnswerDto): Observable<AnswerDto>;
  updateAnswer(quizId: number, answerId: number, data: UpdateAnswerDto): Observable<AnswerDto>;
  deleteAnswer(quizId: number, answerId: number): Observable<boolean>;
  validateAnswer(quizId: number, questionId: number, answerId: number): Observable<ValidateAnswerDto>;
}
```

## NotificationService

```typescript
@Injectable({ providedIn: 'root' })
export class NotificationService {
  private snackBar = inject(MatSnackBar);
  
  success(message: string): void;
  error(message: string): void;
  info(message: string): void;
}
```

---

# 11) Interceptors

## AuthInterceptor

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // Cookie-based auth: браузер автоматично додає cookie
  // Потрібно лише встановити withCredentials для cross-origin запитів
  if (req.url.startsWith('/api')) {
    req = req.clone({
      withCredentials: true
    });
  }
  
  return next(req);
};
```

## ErrorInterceptor

```typescript
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const notification = inject(NotificationService);
  
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        router.navigate(['/auth/login']);
      }
      notification.error(error.error?.detail || 'An error occurred');
      return throwError(() => error);
    })
  );
};
```

---

# 12) Guards

## AuthGuard

```typescript
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  if (authService.isAuthenticated()) {
    return true;
  }
  
  return router.createUrlTree(['/auth/login'], {
    queryParams: { returnUrl: state.url }
  });
};
```

---

# 13) i18n + RTL

## Бібліотека: @ngx-translate/core

**Встановлення:**
```bash
npm install @ngx-translate/core @ngx-translate/http-loader
```

**Конфігурація (app.config.ts):**
```typescript
import { HttpClient, provideHttpClient } from '@angular/common/http';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';

export function HttpLoaderFactory(http: HttpClient) {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    importProvidersFrom(
      TranslateModule.forRoot({
        defaultLanguage: 'uk',
        loader: {
          provide: TranslateLoader,
          useFactory: HttpLoaderFactory,
          deps: [HttpClient]
        }
      })
    )
  ]
};
```

## I18nService

```typescript
@Injectable({ providedIn: 'root' })
export class I18nService {
  private translate = inject(TranslateService);
  
  currentLang = signal<string>('uk');
  
  constructor() {
    const saved = localStorage.getItem('lang') || 'uk';
    this.setLanguage(saved);
  }
  
  setLanguage(lang: string): void {
    this.translate.use(lang);
    this.currentLang.set(lang);
    localStorage.setItem('lang', lang);
    
    // RTL support for Hebrew
    document.documentElement.dir = lang === 'he' ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;
  }
  
  get supportedLanguages(): string[] {
    return ['uk', 'en', 'he'];
  }
}
```

## Використання в компонентах

```typescript
// В template
<h1>{{ 'HOME.TITLE' | translate }}</h1>

// В коді
private translate = inject(TranslateService);
this.translate.instant('ERRORS.INVALID_EMAIL');
```

## Translation Files

```
assets/i18n/
├── uk.json
├── en.json
└── he.json
```

**Приклад uk.json:**
```json
{
  "COMMON": {
    "SAVE": "Зберегти",
    "CANCEL": "Скасувати",
    "DELETE": "Видалити",
    "EDIT": "Редагувати",
    "LOADING": "Завантаження...",
    "NO_DATA": "Немає даних"
  },
  "AUTH": {
    "LOGIN": "Увійти",
    "REGISTER": "Реєстрація",
    "LOGOUT": "Вийти",
    "EMAIL": "Email",
    "PASSWORD": "Пароль",
    "NAME": "Ім'я",
    "SURNAME": "Прізвище"
  },
  "ERRORS": {
    "REQUIRED": "Обов'язкове поле",
    "INVALID_EMAIL": "Невірний формат email",
    "MIN_LENGTH": "Мінімум {{min}} символів",
    "PASSWORDS_MISMATCH": "Паролі не співпадають"
  },
  "QUIZ": {
    "LIST_TITLE": "Мої квізи",
    "CREATE": "Створити квіз",
    "QUESTIONS": "Питання",
    "RUN": "Почати"
  }
}
```

## RTL Support (styles.scss)

```scss
[dir="rtl"] {
  .mat-drawer-container {
    direction: rtl;
  }
  
  .text-start {
    text-align: right !important;
  }
  
  .text-end {
    text-align: left !important;
  }
}
```

---

# 14) Form Validation Rules

## Загальні правила

| Поле | Правила |
|------|---------|
| **email** | Required, Email format, max 255 chars |
| **password** | Required, min 8 chars, max 128 chars |
| **name** | Required, min 2 chars, max 100 chars |
| **surname** | Optional, max 100 chars |
| **quiz.url** | Required, YouTube URL pattern |
| **question.text** | Required, min 10 chars, max 500 chars |
| **answer.text** | Required, min 1 char, max 300 chars |

## Validators

```typescript
export const ValidationPatterns = {
  email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
  youtubeUrl: /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]+/,
  password: /^.{8,128}$/
};

export const ValidationMessages = {
  required: 'ERRORS.REQUIRED',
  email: 'ERRORS.INVALID_EMAIL',
  minlength: 'ERRORS.MIN_LENGTH',
  maxlength: 'ERRORS.MAX_LENGTH',
  pattern: 'ERRORS.INVALID_FORMAT',
  passwordMismatch: 'ERRORS.PASSWORDS_MISMATCH'
};
```

---

# 15) UI States

## Loading States

Кожен async запит повинен мати loading state:

```typescript
interface LoadingState {
  isLoading: signal<boolean>;
  error: signal<string | null>;
}

// Використання в компоненті
isLoading = signal(false);
error = signal<string | null>(null);

async loadData() {
  this.isLoading.set(true);
  this.error.set(null);
  try {
    const data = await firstValueFrom(this.service.getData());
    // handle data
  } catch (e) {
    this.error.set('Failed to load data');
  } finally {
    this.isLoading.set(false);
  }
}
```

**UI паттерн:**
```html
@if (isLoading()) {
  <mat-spinner diameter="40"></mat-spinner>
} @else if (error()) {
  <div class="error">{{ error() }}</div>
} @else {
  <!-- content -->
}
```

## Empty States

| Екран | Empty State Message |
|-------|---------------------|
| Quiz List | "У вас ще немає квізів. Створіть перший!" + CTA button |
| Questions (Edit) | "Квіз не має питань. Додайте перше питання." |
| Answers (Edit) | "Питання не має відповідей. Додайте варіанти." |
| Run Results History | "Ви ще не проходили цей квіз." |

## Confirmation Dialogs

**Потрібно підтвердження для:**
- Delete Quiz
- Delete Question
- Delete Answer
- Logout (optional)

```typescript
// Використання MatDialog
async confirmDelete(item: string): Promise<boolean> {
  const dialogRef = this.dialog.open(ConfirmDialogComponent, {
    data: {
      title: 'COMMON.CONFIRM_DELETE',
      message: `COMMON.DELETE_CONFIRM_MESSAGE`,
      confirmText: 'COMMON.DELETE',
      cancelText: 'COMMON.CANCEL'
    }
  });
  
  return firstValueFrom(dialogRef.afterClosed());
}
```

---

# 16) Acceptance Criteria (Summary)

## Auth

- [ ] Користувач може зареєструватися
- [ ] Користувач може залогінитись
- [ ] Користувач може вийти
- [ ] Приватні сторінки недоступні без токена

## Quizzes

- [ ] Список показує квізи
- [ ] Пошук по назві працює
- [ ] Create створює квіз
- [ ] Edit редагує квіз
- [ ] Delete видаляє квіз

## Questions & Answers

- [ ] Можна додавати/редагувати/видаляти питання
- [ ] Можна додавати/редагувати/видаляти відповіді
- [ ] Можна позначати правильну відповідь

## Run Quiz

- [ ] Питання перемішуються на старті
- [ ] Відповіді зберігаються локально
- [ ] Feedback показується після кожної відповіді
- [ ] Results показують фінальний score

## Local Storage (IndexedDB)

- [ ] Спроби зберігаються
- [ ] Статистика оновлюється
- [ ] Можна продовжити незавершену спробу

## i18n

- [ ] UI доступний uk/en/he
- [ ] RTL для Hebrew працює

---

# 17) Додаткові рекомендації

## Performance

- Lazy loading для feature routes
- `trackBy` для `@for` loops
- `OnPush` change detection

## Accessibility

- WCAG AA compliance
- Focus management
- ARIA attributes
- Color contrast

## Error Handling

**Error Response Format (FastAPI):**
```typescript
interface ErrorResponse {
  detail: string; // Error message from backend
}
```

**HTTP Status Codes:**
| Code | Meaning | Example |
| ---- | ------- | ------- |
| 400  | Bad Request | "User with this email already exists" |
| 401  | Unauthorized | "Invalid credentials" |
| 404  | Not Found | "Question not found" |
| 500  | Server Error | Internal error |

**Frontend Handling:**
- Global `ErrorInterceptor` для відображення помилок
- Redirect на `/auth/login` при 401
- User-friendly повідомлення через `NotificationService`

---

# 18) Resolved Questions

✅ **Answer validation endpoint** — реалізовано:
- Endpoint: `GET /api/quizz/:quizzId/answers/validate/:questionId/:answerId`
- Відповідь: `{ is_correct, description, valid_description }`

✅ **Explanation fields** — реалізовано:
- `description` — пояснення неправильної відповіді
- `valid_description` — пояснення правильної відповіді

✅ **Answer connection** — реалізовано:
- Відповіді отримуються через: `GET /api/quizz/:quizzId/answers`
- Питання отримуються через: `GET /api/quizz/:quizzId/questions`
- Зв'язок: питання → відповіді через `question_id` у моделі

✅ **Quiz creation** — реалізовано:
- Квізи створюються з YouTube URL
- AI автоматично генерує питання та відповіді
- Можна редагувати після створення

✅ **Public API** — реалізовано:
- Всі endpoints доступні через `/api/quizz` (без `/admin`)
- Контроль доступу на бекенді
