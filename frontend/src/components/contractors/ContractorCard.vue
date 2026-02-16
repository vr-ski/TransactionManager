<template>
  <div class="contractor-card" @click="$emit('click')">
    <span class="name">{{ contractor.name }}</span>
    <span class="id">ID: {{ contractor.contractor_id }}</span>
  </div>
</template>

<script setup lang="ts">
import type { Contractor } from "@/types/contractor";
defineProps<{ contractor: Contractor }>();
defineEmits(["click"]);
</script>

<style scoped>
.contractor-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: background 0.2s;
}
.contractor-card:hover {
  background: #f9fafb;
}
.name {
  font-weight: 500;
  color: #1e293b;
}
.id {
  font-size: 0.875rem;
  color: #6b7280;
}
</style>
