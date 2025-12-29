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

| Method | Endpoint               | Request                                 | Response                                                     |
| ------ | ---------------------- | --------------------------------------- | ------------------------------------------------------------ |
| POST   | `/api/auth/login`    | `{ email, password }`                 | `{ message, access_token, user_id, email, name, surname }` |
| POST   | `/api/auth/register` | `{ email, password, name, surname? }` | `{ id, email, name, surname }`                             |

## 4.2 Admin Quizzes

| Method | Endpoint                             | Request                     | Response            |
| ------ | ------------------------------------ | --------------------------- | ------------------- |
| GET    | `/api/admin/quizz?page=0&limit=10` | —                          | `AdminQuizzDto[]` |
| GET    | `/api/admin/quizz/:id`             | —                          | `AdminQuizzDto`   |
| POST   | `/api/admin/quizz`                 | `{ name, description }`   | `AdminQuizzDto`   |
| PUT    | `/api/admin/quizz/:id`             | `{ name?, description? }` | `AdminQuizzDto`   |
| DELETE | `/api/admin/quizz/:id`             | —                          | `AdminQuizzDto`   |

## 4.3 Admin Questions

| Method | Endpoint                                   | Request      | Response          |
| ------ | ------------------------------------------ | ------------ | ----------------- |
| GET    | `/admin/quizz/:id/questions`             | —           | `QuestionDto[]` |
| GET    | `/admin/quizz/:id/questions/:questionId` | —           | `QuestionDto`   |
| POST   | `/admin/quizz/:id/questions`             | `{ text }` | `QuestionDto`   |
| PUT    | `/admin/quizz/:id/questions/:questionId` | `{ text }` | `QuestionDto`   |
| DELETE | `/admin/quizz/:id/questions/:questionId` | —           | `QuestionDto`   |

## 4.4 Admin Answers

| Method | Endpoint                                    | Request                   | Response     |
| ------ | ------------------------------------------- | ------------------------- | ------------ |
| GET    | `/admin/quizz/:quizzId/answers`           | —                        | `Answer[]` |
| POST   | `/admin/quizz/:quizzId/answers`           | `{ text, isCorrect }`   | `Answer`   |
| PUT    | `/admin/quizz/:quizzId/answers/:answerId` | `{ text?, isCorrect? }` | `Answer`   |
| DELETE | `/admin/quizz/:quizzId/answers/:answerId` | —                        | —           |

## 4.5 AI Generation

| Method | Endpoint                     | Description              |
| ------ | ---------------------------- | ------------------------ |
| POST   | `/admin/quizz/ai`          | Create quiz with AI      |
| GET    | `/admin/quizz/ai`          | Get AI-generated quizzes |
| GET    | `/admin/quizz/ai/:quizzId` | Get specific AI quiz     |
| DELETE | `/admin/quizz/ai/:quizzId` | Delete AI quiz           |

## 4.6 Public Quizzes

| Method | Endpoint                              | Response              |
| ------ | ------------------------------------- | --------------------- |
| GET    | `/quizz`                            | All available quizzes |
| GET    | `/quizz/:quizzId`                   | Specific quiz         |
| GET    | `/quizz/:quizzId/answers`           | Answers for quiz      |
| GET    | `/quizz/:quizzId/answers/:answerId` | Specific answer       |

---

# 5) Дані та моделі (Frontend Types)

## 5.1 Auth Types

```typescript
// Request DTOs
interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  email: string;
  password: string;
  name: string;
  surname?: string;
}

// Response DTOs
interface LoginResponse {
  message: string;
  access_token: string;
  user_id: string;
  email: string;
  name: string;
  surname: string;
}

interface PublicUser {
  id: number;
  name: string;
  surname: string;
  email: string;
  created_at?: string;
  updated_at?: string;
}
```

## 5.2 Quiz Types

```typescript
interface AdminQuizz {
  id: number;
  name: string;
  description: string;
  questions_count: number;
  created_at?: string;
  updated_at?: string;
  deleted_at?: string;
}

interface CreateQuizz {
  name: string;
  description: string;
}

interface UpdateQuizz {
  name?: string;
  description?: string;
}
```

## 5.3 Question Types

```typescript
interface Question {
  id: number;
  text: string;
  created_at: string;
  updated_at: string;
  deleted_at?: string;
}

interface CreateQuestion {
  text: string;
}
```

## 5.4 Answer Types

```typescript
interface Answer {
  id: number;
  text: string;
  isCorrect: boolean;
  questionId: number;
}

interface CreateAnswer {
  text: string;
  isCorrect: boolean;
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
- Зберегти `access_token` в localStorage
- Redirect до `/app/quizzes`

**Acceptance:**

- [ ] Невірні креденшали → показати помилку
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
- POST `/auth/register`
- Після успіху → redirect на login або автологін

**Acceptance:**

- [ ] Валідація confirmPassword
- [ ] Існуючий email → помилка "User with this email already exists"
- [ ] Успіх → користувач у системі

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
- Create button

**Логіка:**

- GET `/admin/quizz?page=0&limit=10`
- Client-side filtering по name
- Pagination

**Acceptance:**

- [ ] Пошук працює
- [ ] Create веде на форму
- [ ] Edit/Run/Delete працюють

---

## 9.5 Create Quiz (`/app/quizzes/new`)

**UI:**

- name (input, required)
- description (textarea, required)
- Submit button

**Логіка:**

- POST `/admin/quizz` з `{ name, description }`
- Redirect на список

**Acceptance:**

- [ ] Валідація required полів
- [ ] Успіх → snackbar + redirect

---

## 9.6 Edit Quiz (`/app/quizzes/:id/edit`)

**UI:**

- Заголовок: name
- Список питань (cards/accordion):
  - Question text (input)
  - Answers list:
    - answer text
    - radio "correct"
    - delete answer
  - Add answer
  - Delete question
- Add question
- Save button

**Логіка:**

- GET `/admin/quizz/:id` + GET `/admin/quizz/:id/questions`
- Save → PUT/PATCH endpoints

**Acceptance:**

- [ ] Можна редагувати питання/відповіді
- [ ] Можна додавати/видаляти
- [ ] Save працює

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

# 10) Core Services

## AuthService

```typescript
@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  
  currentUser = signal<PublicUser | null>(null);
  isAuthenticated = computed(() => !!this.currentUser());
  
  login(credentials: LoginRequest): Observable<LoginResponse>;
  register(data: RegisterRequest): Observable<PublicUser>;
  logout(): void;
  getToken(): string | null;
}
```

## QuizService

```typescript
@Injectable({ providedIn: 'root' })
export class QuizService {
  private http = inject(HttpClient);
  
  getQuizzes(page: number, limit: number): Observable<AdminQuizz[]>;
  getQuiz(id: number): Observable<AdminQuizz>;
  createQuiz(data: CreateQuizz): Observable<AdminQuizz>;
  updateQuiz(id: number, data: UpdateQuizz): Observable<AdminQuizz>;
  deleteQuiz(id: number): Observable<void>;
  
  getQuestions(quizId: number): Observable<Question[]>;
  createQuestion(quizId: number, data: CreateQuestion): Observable<Question>;
  updateQuestion(quizId: number, questionId: number, data: CreateQuestion): Observable<Question>;
  deleteQuestion(quizId: number, questionId: number): Observable<void>;
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
  const authService = inject(AuthService);
  const token = authService.getToken();
  
  if (token && req.url.startsWith('/api')) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }
  
  return next(req);
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

## Language Switch

- Перемикач мови в header
- Зберігати в localStorage
- Для `he`: `document.documentElement.dir = 'rtl'`

## Translation Files

```
assets/i18n/
├── uk.json
├── en.json
└── he.json
```

---

# 14) Acceptance Criteria (Summary)

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

# 15) Додаткові рекомендації

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

- Global error handler
- User-friendly error messages
- Retry logic for network errors

---

# 16) TODO / Open Questions

> Ці питання потребують уточнення від бекенду:

1. **Answer validation endpoint** — потрібен endpoint для валідації відповіді:

   - Запит: `{ quizId, questionId, optionId }`
   - Відповідь: `{ isCorrect, correctOptionId, explanation }`
2. **Explanation field** — чи є поле `explanation` у питаннях? Якщо так, де?
3. **Answer connection** — як відповіді прив'язані до питань? Потрібен endpoint:

   - `/admin/quizz/:id/questions/:questionId/answers`
4. **Quiz status** — чи є статус квіза (pending/processing/completed)?
5. **User roles** — чи є роль admin для delete операцій?
