<template>
  <div class="transaction-form">
    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="contractor_from">From Contractor</label>
        <select
          id="contractor_from"
          v-model.number="form.contractor_from_id"
          required
          :disabled="loading.contractors"
        >
          <option value="" disabled>Select contractor</option>
          <option
            v-for="c in contractors"
            :key="c.contractor_id"
            :value="c.contractor_id"
          >
            {{ c.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="contractor_to">To Contractor</label>
        <select
          id="contractor_to"
          v-model.number="form.contractor_to_id"
          required
          :disabled="loading.contractors"
        >
          <option value="" disabled>Select contractor</option>
          <option
            v-for="c in contractors"
            :key="c.contractor_id"
            :value="c.contractor_id"
          >
            {{ c.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="amount">Amount</label>
        <input
          id="amount"
          v-model.number="form.amount"
          type="number"
          step="0.01"
          required
        />
      </div>

      <div class="form-group">
        <label for="status">Status</label>
        <select
          id="status"
          v-model.number="form.status_id"
          required
          :disabled="loading.statuses"
        >
          <option value="" disabled>Select status</option>
          <option v-for="s in statuses" :key="s.status_id" :value="s.status_id">
            {{ s.display_name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="type">Transaction Type</label>
        <select
          id="type"
          v-model.number="form.transaction_type_id"
          required
          :disabled="loading.types"
        >
          <option value="" disabled>Select type</option>
          <option
            v-for="t in transactionTypes"
            :key="t.transaction_type_id"
            :value="t.transaction_type_id"
          >
            {{ t.display_name }}
          </option>
        </select>
      </div>

      <div class="actions">
        <button type="submit" class="submit-btn" :disabled="!formReady">
          Create
        </button>
        <button type="button" class="cancel-btn" @click="resetForm">
          Reset
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, watch, computed } from "vue";
import type { TransactionCreateRequest } from "@/types/transaction";
import type { Contractor } from "@/types/contractor";
import type { Status } from "@/types/status";
import type { TransactionType } from "@/types/transactionType";
import { contractorService } from "@/services/contractorService";
import { statusService } from "@/services/statusService";
import { transactionTypeService } from "@/services/transactionTypeService";
import { useAuthStore } from "@/stores/auth";

const emit = defineEmits<{
  (e: "save", data: TransactionCreateRequest): void;
}>();

const authStore = useAuthStore();

const contractors = ref<Contractor[]>([]);
const statuses = ref<Status[]>([]);
const transactionTypes = ref<TransactionType[]>([]);

const loading = ref({
  contractors: true,
  statuses: true,
  types: true,
});

const form = reactive<TransactionCreateRequest>({
  contractor_from_id: 0,
  contractor_to_id: 0,
  amount: 0,
  status_id: 0,
  transaction_type_id: 0,
});

const formReady = computed(() => {
  return (
    form.contractor_from_id !== 0 &&
    form.contractor_to_id !== 0 &&
    form.amount > 0 &&
    form.status_id !== 0 &&
    form.transaction_type_id !== 0 &&
    !loading.value.contractors &&
    !loading.value.statuses &&
    !loading.value.types
  );
});

// Prefill helpers
function maybePrefillContractors() {
  if (contractors.value.length > 0) {
    if (form.contractor_from_id === 0) {
      form.contractor_from_id = contractors.value[0].contractor_id;
    }
    if (form.contractor_to_id === 0) {
      form.contractor_to_id = contractors.value[0].contractor_id;
    }
  }
}

function maybePrefillStatus() {
  if (statuses.value.length > 0 && form.status_id === 0) {
    form.status_id = statuses.value[0].status_id;
  }
}

function maybePrefillType() {
  if (transactionTypes.value.length > 0 && form.transaction_type_id === 0) {
    form.transaction_type_id = transactionTypes.value[0].transaction_type_id;
  }
}

// Fetch contractors when user is available
async function loadContractors() {
  if (!authStore.user) return;
  loading.value.contractors = true;
  try {
    contractors.value = await contractorService.getByUser(
      authStore.user.user_id,
    );
    maybePrefillContractors();
  } catch (error) {
    console.error("Failed to load contractors:", error);
  } finally {
    loading.value.contractors = false;
  }
}

// Fetch statuses
async function loadStatuses() {
  loading.value.statuses = true;
  try {
    statuses.value = await statusService.getAll();
    maybePrefillStatus();
  } catch (error) {
    console.error("Failed to load statuses:", error);
  } finally {
    loading.value.statuses = false;
  }
}

// Fetch transaction types
async function loadTransactionTypes() {
  loading.value.types = true;
  try {
    transactionTypes.value = await transactionTypeService.getAll();
    maybePrefillType();
  } catch (error) {
    console.error("Failed to load transaction types:", error);
  } finally {
    loading.value.types = false;
  }
}

onMounted(() => {
  loadContractors();
  loadStatuses();
  loadTransactionTypes();
});

watch(
  () => authStore.user,
  (user) => {
    if (user) {
      loadContractors();
    }
  },
  { immediate: true },
);

function resetForm() {
  form.contractor_from_id = 0;
  form.contractor_to_id = 0;
  form.amount = 0;
  form.status_id = 0;
  form.transaction_type_id = 0;
}

function onSubmit() {
  if (!formReady.value) return;
  emit("save", { ...form });
  resetForm();
}
</script>

<style scoped>
.transaction-form {
  background: transparent;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 500;
  color: #4b5563;
}
.form-group select,
.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background: white;
}
.actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}
.submit-btn {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
}
.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.cancel-btn {
  background: #9ca3af;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
}
</style>
