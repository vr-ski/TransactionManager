export interface LoginRequest {
  username: string; // length 5-30
  password: string; // min 8
}

export interface LoginResponse {
  access_token: string;
  refresh_token?: string | null;
  token_type: string;
}
