import { Component, inject, ChangeDetectionStrategy, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from './shared/components/header/header.component';
import { IndexedDbProvider } from './persistence/indexed-db.provider';
import { I18nService } from './core/services/i18n.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HeaderComponent],
  template: `
    <app-header></app-header>
    <main role="main">
      <router-outlet></router-outlet>
    </main>
  `,
  styles: [`
    :host {
      display: block;
    }
  `],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class App implements OnInit {
  private dbProvider = inject(IndexedDbProvider);
  private i18nService = inject(I18nService);

  ngOnInit(): void {
    this.dbProvider.init().catch(err => console.error('Failed to initialize IndexedDB:', err));
  }
}
