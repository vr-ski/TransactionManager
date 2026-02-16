import apiClient from "./api";
import type { LoginRequest, LoginResponse } from "@/types/auth";

export const authService = {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    // Convert credentials to URL-encoded form data
    const formData = new URLSearchParams();
    formData.append("username", credentials.username);
    formData.append("password", credentials.password);

    const response = await apiClient.post<LoginResponse>(
      "/auth/login",
      formData,
      {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      },
    );
    return response.data;
  },
  logout() {
    localStorage.removeItem("access_token");
  },
};
