import { Injectable, inject, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  LoginRequestDto,
  RegisterRequestDto,
  ProfileDto,
  UpdateProfileDto,
  ChangePasswordDto
} from '../models/auth.models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiBasePath}/auth`;

  currentUser = signal<ProfileDto | null>(this.loadUserFromStorage());
  isAuthenticated = computed(() => !!this.currentUser());

  private loadUserFromStorage(): ProfileDto | null {
    try {
      const stored = localStorage.getItem('currentUser');
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  }

  setCurrentUser(user: ProfileDto | null): void {
    this.currentUser.set(user);
    if (user) {
      localStorage.setItem('currentUser', JSON.stringify(user));
    } else {
      localStorage.removeItem('currentUser');
    }
  }

  login(credentials: LoginRequestDto): Observable<ProfileDto> {
    return this.http.post<ProfileDto>(`${this.apiUrl}/login`, credentials);
  }

  register(data: RegisterRequestDto): Observable<boolean> {
    return this.http.post<boolean>(`${this.apiUrl}/register`, data);
  }

  logout(): Observable<boolean> {
    return this.http.post<boolean>(`${this.apiUrl}/logout`, {});
  }

  getProfile(): Observable<ProfileDto> {
    return this.http.get<ProfileDto>(`${this.apiUrl}/profile`);
  }

  updateProfile(data: UpdateProfileDto): Observable<ProfileDto> {
    return this.http.post<ProfileDto>(`${this.apiUrl}/update-profile`, data);
  }

  changePassword(data: ChangePasswordDto): Observable<ProfileDto> {
    return this.http.post<ProfileDto>(`${this.apiUrl}/change-password`, data);
  }
}
