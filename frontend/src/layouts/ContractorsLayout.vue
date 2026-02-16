<template>
  <div class="contractors-layout">
    <!-- Left column: persistent form -->
    <div class="form-section">
      <h2>Create Contractor</h2>
      <ContractorForm @save="createContractor" />
    </div>

    <!-- Right column: dynamic content (list or detail) -->
    <div class="content-section">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import ContractorForm from "@/components/contractors/ContractorForm.vue";
import { useContractorStore } from "@/stores/contractors";
import { useAuthStore } from "@/stores/auth";

const contractorStore = useContractorStore();
const authStore = useAuthStore();

async function createContractor(data: { name: string }) {
  if (!authStore.user) {
    console.error("No authenticated user");
    return;
  }
  await contractorStore.createContractor(authStore.user.user_id, data);
}
</script>

<style scoped>
.contractors-layout {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  align-items: start;
}
.form-section,
.content-section {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}
.form-section h2 {
  margin-bottom: 1.5rem;
  color: #1e293b;
}
@media (max-width: 768px) {
  .contractors-layout {
    grid-template-columns: 1fr;
  }
}
</style>
