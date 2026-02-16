<template>
  <div v-if="transaction" class="transaction-detail-view">
    <h2 class="section-header">
      Transaction #{{ transaction.transaction_id }}
    </h2>
    <div class="detail-card">
      <div class="info-grid">
        <div>
          <span class="label">From:</span> {{ transaction.contractor_from }}
        </div>
        <div>
          <span class="label">To:</span> {{ transaction.contractor_to }}
        </div>
        <div><span class="label">Amount:</span> {{ transaction.amount }}</div>
        <div>
          <span class="label">Type:</span>
          {{ transaction.transaction_type.display_name }}
        </div>
        <div>
          <span class="label">Status:</span>
          <select
            v-model="selectedStatusId"
            @change="updateStatus"
            class="status-select"
            :disabled="updating"
          >
            <option
              v-for="s in statuses"
              :key="s.status_id"
              :value="s.status_id"
            >
              {{ s.display_name }}
            </option>
          </select>
        </div>
        <div>
          <span class="label">Created:</span>
          {{ formatDate(transaction.created_at) }}
        </div>
        <div>
          <span class="label">Updated:</span>
          {{ formatDate(transaction.updated_at) }}
        </div>
      </div>
      <p v-if="updateError" class="error">{{ updateError }}</p>
    </div>
    <button @click="goBack" class="back-btn">← Back to list</button>
  </div>
  <div v-else class="loading">Loading...</div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, computed, watch } from "vue";
import { useTransactionStore } from "@/stores/transactions";
import { useRoute, useRouter } from "vue-router";
import { statusService, type Status } from "@/services/statusService";

const transactionStore = useTransactionStore();
const route = useRoute();
const router = useRouter();

const statuses = ref<Status[]>([]);
const updating = ref(false);
const updateError = ref("");
const selectedStatusId = ref<number | null>(null);

const transaction = computed(() => transactionStore.currentTransaction);

onMounted(async () => {
  const id = Number(route.params.id);
  await Promise.all([transactionStore.fetchTransaction(id), loadStatuses()]);
  if (transaction.value) {
    selectedStatusId.value = transaction.value.status.status_id;
  }
});

onBeforeUnmount(() => {
  transactionStore.currentTransaction = null;
});

watch(transaction, (newTx) => {
  if (newTx) {
    selectedStatusId.value = newTx.status.status_id;
  }
});

async function loadStatuses() {
  try {
    statuses.value = await statusService.getAll();
  } catch (error) {
    console.error("Failed to load statuses:", error);
  }
}

async function updateStatus() {
  if (
    !transaction.value ||
    selectedStatusId.value === transaction.value.status.status_id
  )
    return;

  const newStatusId = selectedStatusId.value!;
  const oldStatusId = transaction.value.status.status_id;

  // Optimistic update
  transactionStore.currentTransaction = {
    ...transaction.value,
    status: {
      ...transaction.value.status,
      status_id: newStatusId,
    },
  };

  updating.value = true;
  updateError.value = "";

  try {
    await transactionStore.updateTransaction(transaction.value.transaction_id, {
      status_id: newStatusId,
    });
  } catch (error: unknown) {
    // Revert
    transactionStore.currentTransaction = {
      ...transaction.value,
      status: {
        ...transaction.value.status,
        status_id: oldStatusId,
      },
    };
    selectedStatusId.value = oldStatusId;
    updateError.value =
      error.response?.data?.detail || "Failed to update status";
  } finally {
    updating.value = false;
  }
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleString();
}

function goBack() {
  router.push("/transactions");
}
</script>

<style scoped>
.transaction-detail-view {
  /* full width */
}
.section-header {
  margin-bottom: 1.5rem;
}
.detail-card {
  background: white;
  border-radius: 0.75rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  margin-bottom: 1rem;
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
.status-select {
  padding: 0.25rem 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: white;
  font-size: 0.875rem;
  margin-left: 0.5rem;
  cursor: pointer;
}
.status-select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}
.status-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.back-btn {
  background: #9ca3af;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.15s ease-in-out;
}
.back-btn:hover {
  background: #6b7280;
}
.error {
  color: #dc2626;
  margin-top: 1rem;
}
.loading {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}
</style>
