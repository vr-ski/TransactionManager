<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/transactions" class="logo"
        >💰 TransactionManager</router-link
      >
      <div class="nav-links" v-if="authStore.isAuthenticated()">
        <router-link to="/transactions">Transactions</router-link>
        <router-link to="/contractors">Contractors</router-link>
        <HealthIndicator />
        <button @click="authStore.logout" class="logout-btn">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import HealthIndicator from "./HealthIndicator.vue";
const authStore = useAuthStore();
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0.75rem 0;
}
.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2563eb;
  text-decoration: none;
}
.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}
.nav-links a {
  color: #4b5563;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}
.nav-links a:hover {
  color: #2563eb;
}
.logout-btn {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.4rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}
.logout-btn:hover {
  background: #dc2626;
}
</style>
