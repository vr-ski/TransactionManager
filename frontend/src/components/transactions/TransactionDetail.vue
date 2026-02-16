<template>
  <div v-if="transaction" class="detail-card">
    <h2>Transaction #{{ transaction.transaction_id }}</h2>
    <div class="info-grid">
      <div>
        <span class="label">From:</span> {{ transaction.contractor_from }}
      </div>
      <div><span class="label">To:</span> {{ transaction.contractor_to }}</div>
      <div><span class="label">Amount:</span> {{ transaction.amount }}</div>
      <div>
        <span class="label">Type:</span> {{ transaction.transaction_type }}
      </div>
      <div>
        <span class="label">Status:</span>
        <span
          class="status-badge"
          :style="{
            backgroundColor: transaction.status.color + '20',
            color: transaction.status.color,
          }"
        >
          {{ transaction.status.display_name }}
        </span>
      </div>
      <div>
        <span class="label">Created:</span>
        {{ new Date(transaction.created_at).toLocaleString() }}
      </div>
      <div>
        <span class="label">Updated:</span>
        {{ new Date(transaction.updated_at).toLocaleString() }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TransactionDetail } from "@/types/transaction";
defineProps<{ transaction: TransactionDetail | null }>();
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
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}
</style>
