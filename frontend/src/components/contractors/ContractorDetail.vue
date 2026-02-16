<template>
  <div class="detail-card" v-if="contractor">
    <div class="info-grid">
      <div><span class="label">Name:</span> {{ contractor.name }}</div>
      <div><span class="label">User ID:</span> {{ contractor.user_id }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Contractor } from "@/types/contractor";
defineProps<{ contractor: Contractor | null }>();
</script>

<style scoped>
.detail-card {
  background: white;
  border-radius: 0.75rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}
.detail-card h2 {
  margin-bottom: 1.5rem;
  color: #1e293b;
}
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}
.info-grid div {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f5f9;
}
.label {
  font-weight: 600;
  color: #4b5563;
  margin-right: 0.5rem;
}
</style>
