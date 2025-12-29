Нижче — **повна специфікація** для імплементації **тільки фронтенду (Angular SPA)** застосунку “Quiz”, з урахуванням усіх ваших уточнень:  **DSNURL** , статуси `pending/processing/completed`,  **редагування правильних відповідей + додавання власних варіантів** ,  **explanation обов’язкова** ,  **shuffle на клієнті** ,  **валідація на бекенді** ,  **збереження статистики/спроб на фронтенді в IndexedDB через обгортку** ,  **пошук по назві + фільтр статусу** ,  **мови uk/en/he (RTL)** .

---

# 1) Мета і межі

## Мета

Зробити SPA, де користувач:

* реєструється/логіниться/виходить
* бачить лендінг із CTA
* керує власними квізами (list/search/filter/create/edit/delete)
* проходить квіз (питання в випадковому порядку, серверна валідація відповіді, проміжний feedback із explanation, фінальні результати)
* має локально збережену історію спроб і статистику по квізах (IndexedDB)

## Межі

* **Тільки фронтенд** .
* Бекенд “існуючий” і доступний на `localhost:8000` через proxy.
* Контракт API може відрізнятись — але фронтенд має бути спроєктований так, щоб **адаптувати шлях/поля в одному місці** (ApiClient + типи).

---

# 2) Технологічні вимоги

* Angular ≥ 17 (standalone components, signals optional)
* Router + Guards
* HttpClient + Interceptors
* Reactive Forms
* RxJS
* UI kit: Angular Material (рекомендовано)
* i18n: uk/en/he
  * Hebrew: RTL (`dir="rtl"`)
* Persistence: IndexedDB **через wrapper** + репозиторії (AttemptRepository / QuizStatsRepository / AppStateRepository)

---

# 3) Конфігурація середовища

## 3.1 Proxy

Фронтенд звертається на `/api/**`, proxy перенаправляє на `http://localhost:8000/**`.

**proxy.conf.json (концепт):**

* context: `/api`
* target: `http://localhost:8000`
* changeOrigin: true
* secure: false

## 3.2 Environment

* `environment.ts`:
  * `apiBasePath: '/api'`
  * `defaultLanguage: 'uk'`
  * `supportedLanguages: ['uk','en','he']`

---

# 4) Ролі, доступ і навігація

## 4.1 Аутентифікація

* Логін/реєстрація через бекенд.
* Токен (accessToken) зберігається на клієнті.
  * мінімально: localStorage
  * (refresh token — якщо бекенд підтримує; інакше — без)
* AuthInterceptor додає `Authorization: Bearer <token>` на всі `/api/**` (крім auth-endpoints якщо треба).

## 4.2 Доступ

* Приватні маршрути під `AuthGuard`.
* Delete —  **адмін-функція** :
  * UI показує Delete лише якщо `user.roles` містить `admin` **або** бекенд у квізі повертає `canDelete=true`.
  * Якщо інформації про роль немає — кнопку Delete не показуємо (safe default).

---

# 5) Дані та моделі (Frontend Contract)

> Назви полів нижче — цільові для фронту. Реальні поля бекенду мапимо через адаптер.

## 5.1 Quiz

* `QuizStatus = 'pending' | 'processing' | 'completed' | 'failed'`
* `QuizSummary`:
  * `id: string`
  * `name: string` *(генерує бекенд)*
  * `dsnUrl: string` *(YouTube URL)*
  * `status: QuizStatus`
  * `createdAt: string`
  * `updatedAt: string`
  * `questionsCount?: number`
* `QuizDetail`:
  * `id, name, dsnUrl, status`
  * `questions: Question[]`
* `Question`:
  * `id: string`
  * `text: string`
  * `explanation: string` ( **required** )
  * `options: AnswerOption[]`
* `AnswerOption`:
  * `id: string`
  * `text: string`
  * `isCorrect: boolean` *(для edit-екрана; у run-флоу не використовувати)*

## 5.2 Run / Attempt (локально)

* `AttemptLocal`:
  * `attemptId: string` (UUID)
  * `quizId: string`
  * `startedAt: number`
  * `finishedAt?: number`
  * `questionOrder: string[]` *(перемішаний порядок questionId)*
  * `answers: AttemptAnswerLocal[]`
  * `score?: number`
  * `total?: number`
* `AttemptAnswerLocal`:
  * `questionId: string`
  * `selectedOptionId: string`
  * `isCorrect: boolean` *(з бекенду)*
  * `correctOptionId?: string` *(з бекенду)*
  * `explanation: string` *(з бекенду або з питання; у вимогах — показувати explanation на feedback)*

## 5.3 Локальна статистика по квізу

* `QuizStatsLocal`:
  * `quizId: string`
  * `attemptsCount: number`
  * `bestScore: number`
  * `lastScore: number`
  * `lastAttemptAt: number`

---

# 6) IndexedDB: повна специфікація persistence

## 6.1 DB

* **DB name:** `quiz_app_db`
* **version:** 1

## 6.2 Object Stores

### `attempts`

* keyPath: `attemptId`
* indexes:
  * `by_quizId` (quizId)
  * `by_startedAt` (startedAt)

### `quiz_stats`

* keyPath: `quizId`
* index:
  * `by_lastAttemptAt` (lastAttemptAt)

### `app_state`

* keyPath: `key`
* записи:
  * `activeAttempt:<quizId>` → `attemptId`

## 6.3 Репозиторії (обов’язкові методи)

### AttemptRepository

* `createAttempt(quizId, questionOrder) -> attemptId`
* `getAttempt(attemptId) -> AttemptLocal | null`
* `appendAnswer(attemptId, answer) -> void`
* `finishAttempt(attemptId, score, total, finishedAt) -> void`
* `listAttemptsByQuiz(quizId, limit=50, offset=0) -> AttemptLocal[]`
* `deleteAttempt(attemptId) -> void`
* `deleteAttemptsByQuiz(quizId) -> void` *(опціонально)*

### QuizStatsRepository

* `getStats(quizId) -> QuizStatsLocal | null`
* `updateAfterAttempt(quizId, score, finishedAt) -> QuizStatsLocal`

### AppStateRepository

* `setActiveAttempt(quizId, attemptId)`
* `getActiveAttempt(quizId) -> attemptId | null`
* `clearActiveAttempt(quizId)`

## 6.4 Політика росту (MVP)

* Зберігати всі спроби (без retention), але **передбачити** опційний cleanup.
* В UI (опціонально): “Очистити історію квіза”.

---

# 7) UX / UI структура

## 7.1 Layout

* Header:
  * Logo → Landing або Quizzes (якщо auth)
  * Language switch: uk/en/he
  * Якщо auth: Quizzes + Logout
  * Якщо no auth: Login/Register
* Main container
* Snackbar/toast для помилок/успіхів

## 7.2 i18n + RTL

* Перемикач мови зберігається локально (localStorage).
* Для `he`:
  * `documentElement.dir = 'rtl'`
  * CSS перевірити в таблицях/формах.

---

# 8) Екрани та поведінка (детально)

## 8.1 Landing (`/`)

**Функціонал:**

* Пояснення продукту
* Кнопки: Login, Register
* Якщо user authenticated: “Go to app”

**Acceptance:**

* Кнопки ведуть на правильні маршрути
* Мова перемикається і зберігається

---

## 8.2 Login (`/auth/login`)

**UI:**

* email, password
* submit
* error message

**Логіка:**

* POST login → токен → redirect to returnUrl або `/app/quizzes`

**Acceptance:**

* Невірні креденшали → показати помилку
* Успішно → доступ до приватних сторінок

---

## 8.3 Register (`/auth/register`)

**UI:**

* email, password, confirmPassword (+ name? якщо бекенд вимагає)
* submit

**Логіка:**

* POST register
* Потім або автологін, або redirect login (за замовчуванням: автологін, якщо бекенд повертає токен)

**Acceptance:**

* Валідація confirmPassword
* Успіх → користувач у системі

---

## 8.4 Quizzes List (`/app/quizzes`)

**UI:**

* Таблиця:
  * Name
  * Status (badge)
  * CreatedAt
  * Local Stats (опціонально: attemptsCount/bestScore)
  * Actions: Edit / Run / Delete
* Search input: пошук по **name**
* Status filter dropdown
* Create button

**Логіка:**

* GET quizzes
* Client-side filtering:
  * `name` contains searchTerm (case-insensitive)
  * status matches selected
* Polling:
  * Для квізів зі статусом `pending|processing` — періодично оновлювати список (5–10 сек)

**Правила доступності кнопок:**

* Run enabled тільки якщо `status == completed`
* Edit enabled тільки якщо `status == completed` *(рекомендовано; якщо треба інакше — змінюється)*
* Delete тільки якщо admin/canDelete

**Acceptance:**

* Пошук + статус фільтр комбінуються
* Pending/processing видно і оновлюються
* Create веде на форму

---

## 8.5 Create Quiz (`/app/quizzes/new`)

**UI:**

* Поле `dsnUrl` (YouTube URL)
* Submit

**Логіка:**

* Валідація:
  * required
  * youtube url pattern
* POST create quiz з `{ dsnUrl }`
* Результат:
  * квіз з’являється зі статусом pending
  * redirect на список або на деталі (в MVP: на список)

**Acceptance:**

* Некоректний URL → помилка під полем
* Успіх → snackbar + квіз у списку

---

## 8.6 Edit Quiz (`/app/quizzes/:id/edit`)

**UI:**

* Заголовок: name + status
* Список питань (accordion/cards)
  * Question text (input/textarea)
  * Explanation (textarea) **required**
  * Options list:
    * option text
    * radio “correct”
    * delete option
  * Add option
  * Delete question
* Add question
* Save

**Бізнес-правила валідації форми:**

* Кожне питання:
  * `text` required
  * `explanation` required
  * `options.length >= 2`
  * рівно 1 option позначений correct (single-choice)
* Порожні/некоректні питання блокують Save

**Збереження:**

* MVP: один “Save” → PUT/PATCH quiz detail (bulk)
* Якщо бекенд тільки по частинах — робимо адаптер:
  * update question
  * update option
  * create/delete question/option

**Acceptance:**

* Неможливо зберегти без explanation
* Можна змінити correct option
* Можна додати власні варіанти відповідей
* Після Save → snackbar success

---

## 8.7 Run Start (`/app/quizzes/:id/run`)

**UI:**

* Назва квіза
* Кількість питань
* Start button
* Якщо є незавершена локальна спроба → “Continue attempt” / “Start new” (рекомендовано)

**Логіка:**

* Отримати quiz detail (питання без correct-логіки для run)
* Згенерувати `attemptId` (UUID)
* Shuffle order questionIds (Fisher–Yates)
* Зберегти AttemptLocal в IndexedDB + app_state activeAttempt
* Redirect до першого питання

**Acceptance:**

* Порядок питань стабільний для конкретної спроби (після reload не змінюється)

---

## 8.8 Question (`/app/quizzes/:id/run/q/:index`)

**UI:**

* Питання + варіанти (radio group)
* Submit
* Показ прогресу: `index+1 / total`

**Логіка:**

* Взяти attempt з IndexedDB
* Взяти questionId по `questionOrder[index]`
* Після submit:
  * виклик бекенду для валідації
  * зберегти результат у attempt.answers
  * перейти на feedback

**Acceptance:**

* Без вибору — submit disabled
* Після submit — не можна повторно сабмітити (lock UI)

---

## 8.9 Feedback (`/app/quizzes/:id/run/feedback`)

**UI:**

* Correct/Incorrect
* Selected option
* Correct option (якщо incorrect)
* Explanation (обов’язково показати)
* Next / Finish

**Логіка:**

* Беремо останню відповідь з attempt.answers
* Next → наступний question route
* Finish → results

**Acceptance:**

* Explanation завжди присутня (якщо бекенд не повернув — fallback на question.explanation)

---

## 8.10 Results (`/app/quizzes/:id/run/results`)

**UI:**

* Score, %
* Список:
  * question text
  * selected option
  * correct option
  * correct/incorrect
  * explanation
* Buttons: Retry, Back to list

**Логіка:**

* Обчислити score локально (з attempt.answers)
* `finishAttempt` в IndexedDB
* `updateAfterAttempt` для quiz_stats
* `clearActiveAttempt`

**Acceptance:**

* Результати зберігаються і доступні після перезавантаження

---

# 9) Сервіси та модулі (структура коду)

## Core

* `ApiClient` (basePath `/api`, typed wrappers)
* `AuthService`
* `AuthInterceptor`
* `AuthGuard`
* `NotificationService` (snackbar)
* `I18nService` (language + RTL)
* `ErrorNormalizer` (API errors → message)

## Features

* `QuizzesService` (list/detail/create/update/delete)
* `RunService` (start attempt, get current question, progress)
* `AnswerValidationService` (validate answer на бекенді)

## Persistence

* `IndexedDbProvider` (ініціалізація db, versioning)
* `AttemptRepository`
* `QuizStatsRepository`
* `AppStateRepository`

---

# 10) API інтеграція (front-end припущення + адаптер)

Оскільки точні ендпоїнти не надані, фіксуємо підхід:

* Всі URL/поля концентруються в одному місці:
  * `api.routes.ts` (шляхи)
  * `api.adapters.ts` (мапінг полів, наприклад `DSNURL` ↔ `dsnUrl`)

**Обов’язкові можливості бекенду (логічні):**

* auth: login/register/me
* quizzes: list, create({dsnUrl}), get detail, update detail, delete
* validate answer: прийняти `{quizId, questionId, optionId}` і повернути `{isCorrect, correctOptionId, explanation}`

---

# 11) Логи/аналітика (MVP)

* dev-only console logging для помилок API
* опціонально: зберігати останню помилку в `app_state` для дебагу

---

# 12) Acceptance Criteria (зведено по системі)

## Auth

* [ ] Користувач може зареєструватися, залогінитись, вийти
* [ ] Приватні сторінки недоступні без токена

## Quizzes

* [ ] Список показує квізи користувача
* [ ] Пошук по назві працює
* [ ] Фільтр по статусу працює
* [ ] Create приймає тільки валідний DSNURL і створює квіз зі статусом pending
* [ ] Polling оновлює статуси pending/processing

## Edit

* [ ] Можна редагувати питання/варіанти/правильну відповідь
* [ ] Можна додавати власні варіанти відповідей
* [ ] Explanation обов’язкова для кожного питання
* [ ] Save блокується при невалідному стані

## Run

* [ ] Питання перемішуються на старті (shuffle client-side) і порядок фіксується для спроби
* [ ] Валідація відповіді відбувається на бекенді
* [ ] Після відповіді показується feedback correct/incorrect + explanation
* [ ] Після завершення — results зі списком питань/відповідей/пояснень

## Local storage (IndexedDB)

* [ ] Спроба і відповіді зберігаються в IndexedDB
* [ ] Статистика по квізу (attemptsCount, bestScore, lastScore, lastAttemptAt) оновлюється локально
* [ ] Після reload можна продовжити активну спробу (якщо не finished)

## i18n

* [ ] UI доступний uk/en/he
* [ ] Для he працює RTL

---

# 13) Що ще все одно треба мати (мінімально) від бекенду

Це єдине, без чого неможливо зробити “під ключ” без ризику переробок:

* назви ендпоїнтів + приклади payload/response (хоча б 1–2 приклади)

Але навіть без цього, за цією специфікацією можна імплементувати:

* повний UI/роутинг/guards/i18n/indexeddb/run-flow
* і залишити “API adapter” як єдину точку підключення реального контракту.

Якщо скинеш приклад відповіді бекенду для **quiz detail** і для **validate answer** — я одразу зафіксую точні DTO та приб’ю всі “TBD” до нуля.
