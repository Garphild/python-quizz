import { Injectable, inject } from '@angular/core';
import { IndexedDbProvider } from './indexed-db.provider';
import { QuizStatsLocal } from '../core/models/attempt.models';

@Injectable({ providedIn: 'root' })
export class QuizStatsRepository {
  private dbProvider = inject(IndexedDbProvider);

  async getStats(quizId: number): Promise<QuizStatsLocal | null> {
    const db = this.dbProvider.getDb();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['quiz_stats'], 'readonly');
      const store = transaction.objectStore('quiz_stats');
      const request = store.get(quizId);

      request.onsuccess = () => resolve(request.result || null);
      request.onerror = () => reject(request.error);
    });
  }

  async updateAfterAttempt(quizId: number, score: number): Promise<QuizStatsLocal> {
    const db = this.dbProvider.getDb();
    const existingStats = await this.getStats(quizId);

    const stats: QuizStatsLocal = existingStats
      ? {
          quizId,
          attemptsCount: existingStats.attemptsCount + 1,
          bestScore: Math.max(existingStats.bestScore, score),
          lastScore: score,
          lastAttemptAt: Date.now()
        }
      : {
          quizId,
          attemptsCount: 1,
          bestScore: score,
          lastScore: score,
          lastAttemptAt: Date.now()
        };

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['quiz_stats'], 'readwrite');
      const store = transaction.objectStore('quiz_stats');
      const request = store.put(stats);

      request.onsuccess = () => resolve(stats);
      request.onerror = () => reject(request.error);
    });
  }
}
