<template>
  <div>
    <h1>Dashboard</h1>
    <p>Welcome!</p>
    <button @click="authStore.logout">Logout</button>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
const authStore = useAuthStore();
</script>
