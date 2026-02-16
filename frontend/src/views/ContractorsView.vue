<template>
  <div>
    <h2 class="section-header">Contractors</h2>
    <div class="list">
      <ContractorCard
        v-for="c in contractorStore.contractors"
        :key="c.contractor_id"
        :contractor="c"
        @click="goToDetail(c.contractor_id)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch } from "vue";
import { useContractorStore } from "@/stores/contractors";
import { useAuthStore } from "@/stores/auth";
import ContractorCard from "@/components/contractors/ContractorCard.vue";
import { useRouter } from "vue-router";

const contractorStore = useContractorStore();
const authStore = useAuthStore();
const router = useRouter();

async function loadContractors() {
  if (authStore.user) {
    await contractorStore.fetchContractors(authStore.user.user_id);
  }
}

watch(() => authStore.user, loadContractors, { immediate: true });

function goToDetail(id: number) {
  router.push(`/contractors/${id}`);
}
</script>

<style scoped>
.list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
/* Removed .section-header override – now relies on global styles */
</style>
