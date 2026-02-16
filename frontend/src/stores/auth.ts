import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authService } from "@/services/authService";
import type { LoginRequest } from "@/types/auth";
import router from "@/router";
import { jwtDecode } from "jwt-decode";

interface TokenPayload {
  sub: string; // user ID
  exp: number;
}

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(localStorage.getItem("access_token"));

  const user = computed(() => {
    if (!token.value) return null;
    try {
      const decoded = jwtDecode<TokenPayload>(token.value);
      return {
        user_id: parseInt(decoded.sub, 10),
      };
    } catch {
      return null;
    }
  });

  async function login(credentials: LoginRequest) {
    const response = await authService.login(credentials);
    localStorage.setItem("access_token", response.access_token);
    token.value = response.access_token;
    await router.push("/transactions");
  }

  function logout() {
    localStorage.removeItem("access_token");
    token.value = null;
    router.push("/login");
  }

  const isAuthenticated = () => !!token.value;

  return { token, user, login, logout, isAuthenticated };
});
