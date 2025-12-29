import { Injectable, inject } from '@angular/core';
import { IndexedDbProvider } from './indexed-db.provider';
import { AttemptLocal, AttemptAnswerLocal } from '../core/models/attempt.models';

@Injectable({ providedIn: 'root' })
export class AttemptRepository {
  private dbProvider = inject(IndexedDbProvider);

  async createAttempt(quizId: number, questionOrder: number[]): Promise<string> {
    const db = this.dbProvider.getDb();
    const attemptId = this.generateUUID();
    const attempt: AttemptLocal = {
      attemptId,
      quizId,
      startedAt: Date.now(),
      questionOrder,
      answers: []
    };

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['attempts'], 'readwrite');
      const store = transaction.objectStore('attempts');
      const request = store.add(attempt);

      request.onsuccess = () => resolve(attemptId);
      request.onerror = () => reject(request.error);
    });
  }

  async getAttempt(attemptId: string): Promise<AttemptLocal | null> {
    const db = this.dbProvider.getDb();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['attempts'], 'readonly');
      const store = transaction.objectStore('attempts');
      const request = store.get(attemptId);

      request.onsuccess = () => resolve(request.result || null);
      request.onerror = () => reject(request.error);
    });
  }

  async appendAnswer(attemptId: string, answer: AttemptAnswerLocal): Promise<void> {
    const attempt = await this.getAttempt(attemptId);
    if (!attempt) {
      throw new Error('Attempt not found');
    }

    attempt.answers.push(answer);

    return new Promise((resolve, reject) => {
      const db = this.dbProvider.getDb();
      const transaction = db.transaction(['attempts'], 'readwrite');
      const store = transaction.objectStore('attempts');
      const request = store.put(attempt);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async finishAttempt(attemptId: string, score: number, total: number): Promise<void> {
    const attempt = await this.getAttempt(attemptId);
    if (!attempt) {
      throw new Error('Attempt not found');
    }

    attempt.finishedAt = Date.now();
    attempt.score = score;
    attempt.total = total;

    return new Promise((resolve, reject) => {
      const db = this.dbProvider.getDb();
      const transaction = db.transaction(['attempts'], 'readwrite');
      const store = transaction.objectStore('attempts');
      const request = store.put(attempt);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async listAttemptsByQuiz(quizId: number, limit?: number): Promise<AttemptLocal[]> {
    const db = this.dbProvider.getDb();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['attempts'], 'readonly');
      const store = transaction.objectStore('attempts');
      const index = store.index('by_quizId');
      const request = index.getAll(quizId);

      request.onsuccess = () => {
        const attempts = request.result as AttemptLocal[];
        const sorted = attempts.sort((a, b) => b.startedAt - a.startedAt);
        resolve(limit ? sorted.slice(0, limit) : sorted);
      };
      request.onerror = () => reject(request.error);
    });
  }

  async deleteAttempt(attemptId: string): Promise<void> {
    const db = this.dbProvider.getDb();

    return new Promise((resolve, reject) => {
      const transaction = db.transaction(['attempts'], 'readwrite');
      const store = transaction.objectStore('attempts');
      const request = store.delete(attemptId);

      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  private generateUUID(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }
}
