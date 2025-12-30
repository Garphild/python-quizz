import { Injectable, inject } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TranslateService } from '@ngx-translate/core';

@Injectable({ providedIn: 'root' })
export class NotificationService {
  private snackBar = inject(MatSnackBar);
  private translate = inject(TranslateService);

  success(message: string, duration: number = 3000): void {
    const translatedMessage = this.translate.instant(message);
    const closeText = this.translate.instant('COMMON.CLOSE');
    this.snackBar.open(translatedMessage, closeText, {
      duration,
      horizontalPosition: 'end',
      verticalPosition: 'bottom',
      panelClass: ['snackbar-success']
    });
  }

  error(message: string, duration: number = 5000): void {
    const translatedMessage = this.translate.instant(message);
    const closeText = this.translate.instant('COMMON.CLOSE');
    this.snackBar.open(translatedMessage, closeText, {
      duration,
      horizontalPosition: 'end',
      verticalPosition: 'bottom',
      panelClass: ['snackbar-error']
    });
  }

  info(message: string, duration: number = 3000): void {
    const translatedMessage = this.translate.instant(message);
    const closeText = this.translate.instant('COMMON.CLOSE');
    this.snackBar.open(translatedMessage, closeText, {
      duration,
      horizontalPosition: 'end',
      verticalPosition: 'bottom',
      panelClass: ['snackbar-info']
    });
  }
}
