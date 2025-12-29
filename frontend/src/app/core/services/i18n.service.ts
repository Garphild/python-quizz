import { Injectable, inject, signal } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class I18nService {
  private translate = inject(TranslateService);

  currentLang = signal<string>(environment.defaultLanguage);

  constructor() {
    const saved = localStorage.getItem('lang') || environment.defaultLanguage;
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
    return environment.supportedLanguages;
  }
}
