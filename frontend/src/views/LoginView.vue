<template>
  <div class="login-view">
    <div class="login-card">
      <h1>💰 TransactionManager</h1>
      <p class="subtitle">Sign in to your account</p>
      <LoginForm />
    </div>
  </div>
</template>

<script setup lang="ts">
import LoginForm from "@/components/auth/LoginForm.vue";
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  padding: 1rem;
}

.login-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.login-card h1 {
  font-size: 1.875rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
  text-align: center;
}

.login-card .subtitle {
  color: #6b7280;
  text-align: center;
  margin-bottom: 2rem;
}
</style>
