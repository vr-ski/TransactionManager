<template>
  <form @submit.prevent="handleSubmit" class="login-form">
    <div class="form-group">
      <label for="username">Username</label>
      <input
        id="username"
        v-model="form.username"
        type="text"
        required
        placeholder="Enter your username"
        :disabled="loading"
      />
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <input
        id="password"
        v-model="form.password"
        type="password"
        required
        placeholder="Enter your password"
        :disabled="loading"
      />
    </div>

    <button type="submit" class="submit-btn" :disabled="loading">
      <span v-if="loading">Signing in...</span>
      <span v-else>Sign In</span>
    </button>

    <p v-if="error" class="error">{{ error }}</p>
    <pre v-if="detailedError" class="error-detail">{{ detailedError }}</pre>
  </form>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const form = ref({ username: "", password: "" });
const loading = ref(false);
const error = ref("");
const detailedError = ref("");

async function handleSubmit() {
  loading.value = true;
  error.value = "";
  detailedError.value = "";
  try {
    await authStore.login(form.value);
  } catch (err: unknown) {
    if (err.response) {
      error.value = `Error ${err.response.status}: ${err.response.statusText}`;
      if (err.response.data) {
        detailedError.value = JSON.stringify(err.response.data, null, 2);
      }
    } else if (err.request) {
      error.value = "No response from server. Please check your connection.";
    } else {
      error.value = err.message;
    }
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.form-group label {
  font-weight: 500;
  color: #4b5563;
  font-size: 0.875rem;
}

.form-group input {
  padding: 0.625rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition:
    border-color 0.15s ease-in-out,
    box-shadow 0.15s ease-in-out;
}

.form-group input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-group input:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}

.submit-btn {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.15s ease-in-out;
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  background: #1d4ed8;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #dc2626;
  font-size: 0.875rem;
  text-align: center;
  margin-top: 0.5rem;
}

.error-detail {
  color: #991b1b;
  background: #fee2e2;
  padding: 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  white-space: pre-wrap;
  margin-top: 0.5rem;
}
</style>
