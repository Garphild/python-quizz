# Quiz App — Brandbook & Style Guide

> Брендбук та стайлгайд для Angular фронтенду Quiz Application

---

## 1. Бренд

### 1.1 Назва продукту

**Quiz App** — платформа для створення та проходження квізів на основі YouTube відео з AI-генерацією питань.

### 1.2 Місія

Зробити навчання інтерактивним та доступним через автоматичну генерацію квізів з відеоконтенту.

### 1.3 Цінності бренду

- **Простота** — мінімалістичний інтерфейс без зайвих елементів
- **Доступність** — підтримка різних мов та RTL
- **Надійність** — стабільна робота офлайн через IndexedDB
- **Інтелект** — AI-powered генерація контенту

### 1.4 Тон комунікації

- Дружній, але професійний
- Лаконічний та зрозумілий
- Підтримуючий користувача

---

## 2. Кольорова палітра

### 2.1 Основні кольори (Primary)

| Назва | HEX | RGB | Використання |
|-------|-----|-----|--------------|
| **Primary** | `#1976D2` | rgb(25, 118, 210) | Основні кнопки, посилання, акценти |
| **Primary Light** | `#42A5F5` | rgb(66, 165, 245) | Hover states, secondary actions |
| **Primary Dark** | `#1565C0` | rgb(21, 101, 192) | Active states, headers |

### 2.2 Акцентні кольори (Accent)

| Назва | HEX | RGB | Використання |
|-------|-----|-----|--------------|
| **Accent** | `#FF4081` | rgb(255, 64, 129) | CTA кнопки, важливі елементи |
| **Accent Light** | `#FF80AB` | rgb(255, 128, 171) | Hover на accent |
| **Accent Dark** | `#F50057` | rgb(245, 0, 87) | Active на accent |

### 2.3 Семантичні кольори

| Назва | HEX | RGB | Використання |
|-------|-----|-----|--------------|
| **Success** | `#4CAF50` | rgb(76, 175, 80) | Правильні відповіді, успішні дії |
| **Error** | `#F44336` | rgb(244, 67, 54) | Помилки, неправильні відповіді |
| **Warning** | `#FF9800` | rgb(255, 152, 0) | Попередження, увага |
| **Info** | `#2196F3` | rgb(33, 150, 243) | Інформаційні повідомлення |

### 2.4 Нейтральні кольори

| Назва | HEX | RGB | Використання |
|-------|-----|-----|--------------|
| **Background** | `#F5F5F5` | rgb(245, 245, 245) | Фон сторінки |
| **Surface** | `#FFFFFF` | rgb(255, 255, 255) | Картки, діалоги |
| **Text Primary** | `#212121` | rgb(33, 33, 33) | Основний текст |
| **Text Secondary** | `#757575` | rgb(117, 117, 117) | Вторинний текст |
| **Divider** | `#E0E0E0` | rgb(224, 224, 224) | Розділювачі, бордери |
| **Disabled** | `#9E9E9E` | rgb(158, 158, 158) | Неактивні елементи |

### 2.5 CSS Variables

```css
:root {
  /* Primary */
  --color-primary: #1976D2;
  --color-primary-light: #42A5F5;
  --color-primary-dark: #1565C0;
  --color-primary-contrast: #FFFFFF;

  /* Accent */
  --color-accent: #FF4081;
  --color-accent-light: #FF80AB;
  --color-accent-dark: #F50057;
  --color-accent-contrast: #FFFFFF;

  /* Semantic */
  --color-success: #4CAF50;
  --color-error: #F44336;
  --color-warning: #FF9800;
  --color-info: #2196F3;

  /* Neutral */
  --color-background: #F5F5F5;
  --color-surface: #FFFFFF;
  --color-text-primary: #212121;
  --color-text-secondary: #757575;
  --color-divider: #E0E0E0;
  --color-disabled: #9E9E9E;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
  --shadow-md: 0 3px 6px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 10px 20px rgba(0, 0, 0, 0.15), 0 3px 6px rgba(0, 0, 0, 0.10);
}
```

### 2.6 Контраст та доступність

Всі комбінації кольорів відповідають WCAG AA:

| Комбінація | Контраст | Статус |
|------------|----------|--------|
| Primary на White | 4.5:1 | ✅ AA |
| Text Primary на Background | 12.6:1 | ✅ AAA |
| Text Secondary на Background | 4.6:1 | ✅ AA |
| Success на White | 3.0:1 | ⚠️ Large text only |
| Error на White | 4.0:1 | ✅ AA (large text) |

---

## 3. Типографіка

### 3.1 Шрифти

| Тип | Шрифт | Fallback |
|-----|-------|----------|
| **Primary** | Roboto | "Helvetica Neue", Arial, sans-serif |
| **Monospace** | Roboto Mono | Consolas, Monaco, monospace |
| **Hebrew (RTL)** | Heebo | Arial, sans-serif |

### 3.2 Розміри шрифтів

| Назва | Розмір | Line Height | Використання |
|-------|--------|-------------|--------------|
| **Display** | 56px | 1.2 | Hero заголовки |
| **H1** | 32px | 1.25 | Заголовки сторінок |
| **H2** | 24px | 1.3 | Секції |
| **H3** | 20px | 1.4 | Підзаголовки |
| **H4** | 18px | 1.4 | Card headers |
| **Body 1** | 16px | 1.5 | Основний текст |
| **Body 2** | 14px | 1.5 | Вторинний текст |
| **Caption** | 12px | 1.4 | Підписи, hints |
| **Button** | 14px | 1.15 | Кнопки (uppercase) |

### 3.3 Font Weights

| Назва | Weight | Використання |
|-------|--------|--------------|
| **Light** | 300 | Display text |
| **Regular** | 400 | Body text |
| **Medium** | 500 | Buttons, labels |
| **Bold** | 700 | Headers, emphasis |

### 3.4 CSS Typography

```css
/* Typography Scale */
:root {
  --font-family-primary: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  --font-family-mono: 'Roboto Mono', Consolas, Monaco, monospace;
  --font-family-hebrew: 'Heebo', Arial, sans-serif;

  --font-size-display: 3.5rem;    /* 56px */
  --font-size-h1: 2rem;           /* 32px */
  --font-size-h2: 1.5rem;         /* 24px */
  --font-size-h3: 1.25rem;        /* 20px */
  --font-size-h4: 1.125rem;       /* 18px */
  --font-size-body1: 1rem;        /* 16px */
  --font-size-body2: 0.875rem;    /* 14px */
  --font-size-caption: 0.75rem;   /* 12px */

  --font-weight-light: 300;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;

  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-loose: 1.75;
}

/* RTL Typography */
[dir="rtl"] {
  font-family: var(--font-family-hebrew);
}
```

---

## 4. Spacing System

### 4.1 Base Unit

**Base unit: 8px** — всі відступи кратні 8.

### 4.2 Spacing Scale

| Token | Value | Використання |
|-------|-------|--------------|
| `--spacing-0` | 0px | — |
| `--spacing-1` | 4px | Мінімальний padding |
| `--spacing-2` | 8px | Icon spacing |
| `--spacing-3` | 12px | Tight padding |
| `--spacing-4` | 16px | Default padding |
| `--spacing-5` | 20px | Card padding |
| `--spacing-6` | 24px | Section spacing |
| `--spacing-8` | 32px | Large spacing |
| `--spacing-10` | 40px | XL spacing |
| `--spacing-12` | 48px | Page margins |
| `--spacing-16` | 64px | Section gaps |

### 4.3 CSS Spacing

```css
:root {
  --spacing-1: 0.25rem;   /* 4px */
  --spacing-2: 0.5rem;    /* 8px */
  --spacing-3: 0.75rem;   /* 12px */
  --spacing-4: 1rem;      /* 16px */
  --spacing-5: 1.25rem;   /* 20px */
  --spacing-6: 1.5rem;    /* 24px */
  --spacing-8: 2rem;      /* 32px */
  --spacing-10: 2.5rem;   /* 40px */
  --spacing-12: 3rem;     /* 48px */
  --spacing-16: 4rem;     /* 64px */
}
```

---

## 5. Breakpoints (Responsive)

### 5.1 Breakpoint Scale

| Назва | Min Width | Max Width | Target |
|-------|-----------|-----------|--------|
| **xs** | 0px | 599px | Mobile portrait |
| **sm** | 600px | 959px | Mobile landscape, small tablets |
| **md** | 960px | 1279px | Tablets, small laptops |
| **lg** | 1280px | 1919px | Laptops, desktops |
| **xl** | 1920px | ∞ | Large monitors |

### 5.2 CSS Media Queries

```css
/* Mobile First Approach */
@media (min-width: 600px) { /* sm */ }
@media (min-width: 960px) { /* md */ }
@media (min-width: 1280px) { /* lg */ }
@media (min-width: 1920px) { /* xl */ }

/* Max-width for specific overrides */
@media (max-width: 599px) { /* xs only */ }
```

### 5.3 Layout Guidelines

| Screen | Max Container | Columns | Gutter |
|--------|---------------|---------|--------|
| xs | 100% | 4 | 16px |
| sm | 100% | 8 | 16px |
| md | 840px | 12 | 24px |
| lg | 1140px | 12 | 24px |
| xl | 1440px | 12 | 32px |

---

## 6. Компоненти UI

### 6.1 Buttons

#### Primary Button
```scss
.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-primary-contrast);
  padding: var(--spacing-3) var(--spacing-6);
  border-radius: 4px;
  font-weight: var(--font-weight-medium);
  font-size: var(--font-size-body2);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;

  &:hover {
    background-color: var(--color-primary-dark);
    box-shadow: var(--shadow-md);
  }

  &:focus {
    outline: 2px solid var(--color-primary-light);
    outline-offset: 2px;
  }

  &:disabled {
    background-color: var(--color-disabled);
    cursor: not-allowed;
    box-shadow: none;
  }
}
```

#### Button Variants

| Variant | Background | Text | Border |
|---------|------------|------|--------|
| Primary | `--color-primary` | white | none |
| Secondary | transparent | `--color-primary` | 1px primary |
| Accent | `--color-accent` | white | none |
| Warn | `--color-error` | white | none |
| Text | transparent | `--color-primary` | none |

#### Button Sizes

| Size | Height | Padding | Font |
|------|--------|---------|------|
| Small | 32px | 8px 16px | 12px |
| Medium | 40px | 12px 24px | 14px |
| Large | 48px | 16px 32px | 16px |

### 6.2 Form Fields

#### Input Field
```scss
.form-field {
  width: 100%;
  margin-bottom: var(--spacing-5);

  label {
    display: block;
    font-size: var(--font-size-caption);
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-1);
    font-weight: var(--font-weight-medium);
  }

  input, textarea {
    width: 100%;
    padding: var(--spacing-3) var(--spacing-4);
    border: 1px solid var(--color-divider);
    border-radius: 4px;
    font-size: var(--font-size-body1);
    font-family: inherit;
    transition: border-color 0.2s ease;

    &:focus {
      outline: none;
      border-color: var(--color-primary);
      box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
    }

    &.error {
      border-color: var(--color-error);
    }
  }

  .error-message {
    font-size: var(--font-size-caption);
    color: var(--color-error);
    margin-top: var(--spacing-1);
  }
}
```

### 6.3 Cards

```scss
.card {
  background: var(--color-surface);
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;

  &-header {
    padding: var(--spacing-5);
    border-bottom: 1px solid var(--color-divider);

    &-title {
      font-size: var(--font-size-h4);
      font-weight: var(--font-weight-medium);
      margin: 0;
    }
  }

  &-content {
    padding: var(--spacing-5);
  }

  &-actions {
    padding: var(--spacing-4) var(--spacing-5);
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-3);
    border-top: 1px solid var(--color-divider);
  }
}
```

### 6.4 Tables

```scss
.table {
  width: 100%;
  border-collapse: collapse;

  th {
    background-color: var(--color-background);
    padding: var(--spacing-4);
    text-align: left;
    font-weight: var(--font-weight-medium);
    font-size: var(--font-size-body2);
    color: var(--color-text-secondary);
    border-bottom: 2px solid var(--color-divider);
  }

  td {
    padding: var(--spacing-4);
    border-bottom: 1px solid var(--color-divider);
    font-size: var(--font-size-body1);
  }

  tr:hover {
    background-color: rgba(0, 0, 0, 0.02);
  }
}
```

### 6.5 Dialogs

```scss
.dialog {
  background: var(--color-surface);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  max-width: 400px;
  width: 90%;

  &-title {
    font-size: var(--font-size-h3);
    font-weight: var(--font-weight-medium);
    padding: var(--spacing-6) var(--spacing-6) var(--spacing-4);
    margin: 0;
  }

  &-content {
    padding: 0 var(--spacing-6) var(--spacing-6);
    color: var(--color-text-secondary);
  }

  &-actions {
    padding: var(--spacing-4) var(--spacing-6);
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-3);
  }
}

.dialog-backdrop {
  background: rgba(0, 0, 0, 0.5);
}
```

### 6.6 Snackbar / Toast

```scss
.snackbar {
  position: fixed;
  bottom: var(--spacing-6);
  right: var(--spacing-6);
  padding: var(--spacing-4) var(--spacing-5);
  border-radius: 4px;
  color: white;
  font-size: var(--font-size-body2);
  box-shadow: var(--shadow-md);
  z-index: 1000;

  &.success { background-color: var(--color-success); }
  &.error { background-color: var(--color-error); }
  &.info { background-color: var(--color-info); }
  &.warning { background-color: var(--color-warning); }
}
```

---

## 7. Icons

### 7.1 Icon System

**Бібліотека:** Material Icons

### 7.2 Icon Sizes

| Size | Dimension | Використання |
|------|-----------|--------------|
| Small | 18px | Inline icons |
| Default | 24px | Buttons, lists |
| Large | 36px | Headers, empty states |
| XL | 48px | Hero sections |

### 7.3 Semantic Icons

| Контекст | Icon | Код |
|----------|------|-----|
| Success | ✓ | `check_circle` |
| Error | ✗ | `error` |
| Warning | ⚠ | `warning` |
| Info | ℹ | `info` |
| Delete | 🗑 | `delete` |
| Edit | ✏ | `edit` |
| Add | + | `add` |
| Close | × | `close` |
| Menu | ☰ | `menu` |
| User | 👤 | `person` |
| Logout | ⎋ | `logout` |
| Play | ▶ | `play_arrow` |
| Language | 🌐 | `language` |

---

## 8. States

### 8.1 Interactive States

| State | Transformation |
|-------|----------------|
| **Default** | Base styles |
| **Hover** | Darken 10%, add shadow |
| **Focus** | 2px outline, offset 2px |
| **Active** | Darken 15% |
| **Disabled** | 60% opacity, no pointer |
| **Loading** | Spinner overlay |

### 8.2 Validation States

| State | Border | Icon | Message Color |
|-------|--------|------|---------------|
| **Valid** | `--color-success` | `check` | success |
| **Invalid** | `--color-error` | `error` | error |
| **Pending** | `--color-warning` | `hourglass` | warning |

### 8.3 Empty States

```html
<div class="empty-state">
  <mat-icon class="empty-icon">quiz</mat-icon>
  <h3>No quizzes yet</h3>
  <p>Create your first quiz from a YouTube video</p>
  <button mat-raised-button color="primary">Create Quiz</button>
</div>
```

```scss
.empty-state {
  text-align: center;
  padding: var(--spacing-16) var(--spacing-6);

  .empty-icon {
    font-size: 64px;
    width: 64px;
    height: 64px;
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-6);
  }

  h3 {
    font-size: var(--font-size-h3);
    margin-bottom: var(--spacing-3);
  }

  p {
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-6);
  }
}
```

---

## 9. Motion & Animation

### 9.1 Duration

| Type | Duration | Easing |
|------|----------|--------|
| Fast | 150ms | ease-out |
| Normal | 300ms | ease-in-out |
| Slow | 500ms | ease-in-out |

### 9.2 CSS Transitions

```css
:root {
  --transition-fast: 150ms ease-out;
  --transition-normal: 300ms ease-in-out;
  --transition-slow: 500ms ease-in-out;
}

/* Usage */
.button {
  transition: background-color var(--transition-fast),
              box-shadow var(--transition-fast);
}

.card {
  transition: transform var(--transition-normal),
              box-shadow var(--transition-normal);
}
```

### 9.3 Animations

```scss
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.fade-in { animation: fadeIn var(--transition-normal); }
.slide-up { animation: slideUp var(--transition-normal); }
.loading-spinner { animation: spin 1s linear infinite; }
```

---

## 10. RTL Support

### 10.1 Direction

```css
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}
```

### 10.2 Logical Properties

Використовуй логічні властивості замість physical:

| Physical | Logical |
|----------|---------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `left` | `inset-inline-start` |
| `right` | `inset-inline-end` |
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |

### 10.3 RTL Overrides

```scss
[dir="rtl"] {
  .icon-button {
    transform: scaleX(-1);
  }

  .progress-bar {
    direction: ltr; /* Keep progress direction */
  }
}
```

---

## 11. Accessibility

### 11.1 Focus Management

```css
/* Focus visible for keyboard navigation */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove focus for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

### 11.2 Screen Reader

```html
<!-- Skip link -->
<a class="skip-link" href="#main-content">Skip to main content</a>

<!-- ARIA labels -->
<button aria-label="Close dialog">×</button>
<input aria-describedby="email-hint" />
<span id="email-hint" class="sr-only">Enter your email address</span>
```

### 11.3 Color Contrast

Мінімальні вимоги WCAG AA:
- **Normal text**: 4.5:1
- **Large text (18px+)**: 3:1
- **UI components**: 3:1

---

## 12. File Structure

```
src/
├── styles/
│   ├── _variables.scss      # CSS variables
│   ├── _typography.scss     # Font styles
│   ├── _spacing.scss        # Spacing utilities
│   ├── _colors.scss         # Color utilities
│   ├── _components.scss     # Component styles
│   ├── _animations.scss     # Keyframes
│   ├── _rtl.scss            # RTL overrides
│   ├── _accessibility.scss  # A11y helpers
│   └── styles.scss          # Main entry point
```

---

## 13. Material Theme

### 13.1 Custom Theme

```scss
@use '@angular/material' as mat;

$quiz-primary: mat.define-palette(mat.$blue-palette, 700);
$quiz-accent: mat.define-palette(mat.$pink-palette, A200);
$quiz-warn: mat.define-palette(mat.$red-palette);

$quiz-theme: mat.define-light-theme((
  color: (
    primary: $quiz-primary,
    accent: $quiz-accent,
    warn: $quiz-warn,
  ),
  typography: mat.define-typography-config(
    $font-family: 'Roboto, "Helvetica Neue", sans-serif',
  ),
  density: 0,
));

@include mat.all-component-themes($quiz-theme);
```

---

## 14. Checklist

### Design Review

- [ ] Всі кольори відповідають палітрі
- [ ] Типографіка консистентна
- [ ] Spacing кратний 8px
- [ ] Responsive на всіх breakpoints
- [ ] RTL підтримка для Hebrew
- [ ] Focus visible для всіх interactive elements
- [ ] Color contrast ≥ 4.5:1 для тексту
- [ ] ARIA labels для всіх icons
- [ ] Loading states для async operations
- [ ] Empty states для порожніх списків
- [ ] Error states для форм

---

**Version:** 1.0.0  
**Last Updated:** December 2024  
**Author:** Quiz App Team
