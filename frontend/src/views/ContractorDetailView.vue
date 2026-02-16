<template>
  <div v-if="contractorStore.currentContractor" class="contractor-detail-view">
    <h2 class="section-header">
      Contractor #{{ contractorStore.currentContractor.contractor_id }}
    </h2>
    <ContractorDetail :contractor="contractorStore.currentContractor" />
    <button @click="goBack" class="back-btn">← Back to list</button>
  </div>
  <div v-else class="loading">Loading...</div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount } from "vue";
import { useContractorStore } from "@/stores/contractors";
import ContractorDetail from "@/components/contractors/ContractorDetail.vue";
import { useRoute, useRouter } from "vue-router";

const contractorStore = useContractorStore();
const route = useRoute();
const router = useRouter();

onMounted(async () => {
  const id = Number(route.params.id);
  await contractorStore.fetchContractor(id);
});

onBeforeUnmount(() => {
  // Clear current contractor to avoid flash of stale data
  contractorStore.currentContractor = null;
});

function goBack() {
  router.push("/contractors");
}
</script>

<style scoped>
.contractor-detail-view {
  /* Remove max-width constraint */
}
.section-header {
  margin-bottom: 1.5rem;
}
.back-btn {
  background: #9ca3af;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  margin-top: 1rem;
}
.back-btn:hover {
  background: #6b7280;
}
.loading {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}
</style>
