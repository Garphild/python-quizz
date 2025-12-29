import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class IndexedDbProvider {
  private db: IDBDatabase | null = null;
  private readonly dbName = 'quiz_app_db';
  private readonly dbVersion = 1;

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.dbVersion);

      request.onerror = () => {
        reject(request.error);
      };

      request.onsuccess = () => {
        this.db = request.result;
        resolve();
      };

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;

        // Create attempts store
        if (!db.objectStoreNames.contains('attempts')) {
          const attemptsStore = db.createObjectStore('attempts', { keyPath: 'attemptId' });
          attemptsStore.createIndex('by_quizId', 'quizId', { unique: false });
          attemptsStore.createIndex('by_startedAt', 'startedAt', { unique: false });
        }

        // Create quiz_stats store
        if (!db.objectStoreNames.contains('quiz_stats')) {
          const statsStore = db.createObjectStore('quiz_stats', { keyPath: 'quizId' });
          statsStore.createIndex('by_lastAttemptAt', 'lastAttemptAt', { unique: false });
        }

        // Create app_state store
        if (!db.objectStoreNames.contains('app_state')) {
          db.createObjectStore('app_state', { keyPath: 'key' });
        }
      };
    });
  }

  getDb(): IDBDatabase {
    if (!this.db) {
      throw new Error('IndexedDB not initialized. Call init() first.');
    }
    return this.db;
  }
}
