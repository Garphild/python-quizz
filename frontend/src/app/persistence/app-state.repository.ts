import { Injectable, inject } from '@angular/core';
import { IndexedDbProvider } from './indexed-db.provider';

@Injectable({ providedIn: 'root' })
export class AppStateRepository {
  private dbProvider = inject(IndexedDbProvider);

  async setActiveAttempt(quizId: number, attemptId: string): Promise<void> {
    const db = this.dbProvider.getDb();
    const key = `activeAttempt:${quizId}`;

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['app_state'], 'readwrite');
      const store = transaction.objectStore('app_state');
      const request = store.put({ key, value: attemptId });

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async getActiveAttempt(quizId: number): Promise<string | null> {
    const db = this.dbProvider.getDb();
    const key = `activeAttempt:${quizId}`;

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['app_state'], 'readonly');
      const store = transaction.objectStore('app_state');
      const request = store.get(key);

      request.onsuccess = () => {
        const result = request.result;
        resolve(result ? result.value : null);
      };
      request.onerror = () => reject(request.error);
    });
  }

  async clearActiveAttempt(quizId: number): Promise<void> {
    const db = this.dbProvider.getDb();
    const key = `activeAttempt:${quizId}`;

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['app_state'], 'readwrite');
      const store = transaction.objectStore('app_state');
      const request = store.delete(key);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }
}
