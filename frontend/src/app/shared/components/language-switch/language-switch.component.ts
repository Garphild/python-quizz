import { Component, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { I18nService } from '../../../core/services/i18n.service';

@Component({
  selector: 'app-language-switch',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatMenuModule, MatIconModule],
  template: `
    <button mat-icon-button [matMenuTriggerFor]="langMenu" aria-label="Language">
      <mat-icon>language</mat-icon>
    </button>
    <mat-menu #langMenu="matMenu">
      @for (lang of i18nService.supportedLanguages; track lang) {
        <button 
          mat-menu-item 
          (click)="i18nService.setLanguage(lang)"
          [class.active]="i18nService.currentLang() === lang">
          {{ getLangName(lang) }}
        </button>
      }
    </mat-menu>
  `,
  styles: [`
    .active {
      font-weight: bold;
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LanguageSwitchComponent {
  i18nService = inject(I18nService);

  getLangName(lang: string): string {
    const names: Record<string, string> = {
      uk: 'Українська',
      en: 'English',
      he: 'עברית'
    };
    return names[lang] || lang;
  }
}
