<template>
  <div class="transactions-layout">
    <!-- Left column: persistent form -->
    <div class="form-section">
      <h2>Make a Transfer</h2>
      <TransactionForm @save="createTransaction" />
    </div>

    <!-- Right column: dynamic content (list or detail) -->
    <div class="content-section">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import TransactionForm from "@/components/transactions/TransactionForm.vue";
import { useTransactionStore } from "@/stores/transactions";

const transactionStore = useTransactionStore();

async function createTransaction(data: TransactionCreateRequest) {
  await transactionStore.createTransaction(data);
}
</script>

<style scoped>
.transactions-layout {
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
  .transactions-layout {
    grid-template-columns: 1fr;
  }
}
</style>
