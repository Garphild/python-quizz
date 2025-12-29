export interface LoginRequestDto {
  email: string;
  password: string;
}

export interface RegisterRequestDto {
  email: string;
  password: string;
  name: string;
  surname?: string;
}

export interface UpdateProfileDto {
  name?: string;
  surname?: string;
}

export interface ChangePasswordDto {
  old_password: string;
  new_password: string;
}

export interface ProfileDto {
  id: number;
  email: string;
  name: string;
  surname?: string;
}
