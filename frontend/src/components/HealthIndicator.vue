<template>
  <div class="health-indicator" :class="status">
    <span class="dot"></span>
    <span class="label">{{
      status === "healthy" ? "API Online" : "API Offline"
    }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { healthService } from "@/services/healthService";

const status = ref<"healthy" | "unhealthy">("healthy");
let interval: number;

async function checkHealth() {
  try {
    await healthService.checkHealth();
    status.value = "healthy";
  } catch {
    status.value = "unhealthy";
  }
}

onMounted(() => {
  checkHealth();
  interval = setInterval(checkHealth, 60000);
});

onUnmounted(() => {
  clearInterval(interval);
});
</script>

<style scoped>
.health-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  background: #f3f4f6;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.healthy .dot {
  background: #10b981;
  box-shadow: 0 0 0 2px #10b98133;
}
.unhealthy .dot {
  background: #ef4444;
  box-shadow: 0 0 0 2px #ef444433;
}
.label {
  color: #4b5563;
}
</style>
