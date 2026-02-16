<template>
  <div class="transaction-list">
    <div v-if="transactions.length === 0" class="empty">
      No transactions yet.
    </div>
    <div v-else class="list">
      <div
        v-for="tx in transactions"
        :key="tx.transaction_id"
        class="transaction-item"
        :class="{ selected: tx.transaction_id === selectedId }"
        @click="$emit('select', tx.transaction_id)"
      >
        <div class="date">{{ formatDate(tx.created_at) }}</div>
        <div class="contractors">
          {{ tx.contractor_from }} → {{ tx.contractor_to }}
        </div>
        <div class="type-amount">
          <span class="type">{{ tx.transaction_type }}</span>
          <span class="amount">{{ tx.amount }}</span>
        </div>
        <div
          class="status"
          :style="{
            backgroundColor: tx.status.color + '20',
            color: tx.status.color,
          }"
        >
          {{ tx.status.display_name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TransactionListItem } from "@/types/transaction";

defineProps<{
  transactions: TransactionListItem[];
  selectedId?: number | null;
}>();

defineEmits<{ (e: "select", id: number): void }>();

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}
</script>

<style scoped>
.transaction-list .list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.transaction-item {
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
.transaction-item:hover {
  background: #f9fafb;
}
.date {
  font-size: 0.875rem;
  color: #6b7280;
  min-width: 100px; /* adjust as needed */
}
.contractors {
  font-weight: 500;
  flex: 1;
  margin-left: 1rem;
}
.type-amount {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin: 0 1rem;
}
.type {
  font-size: 0.875rem;
  color: #6b7280;
}
.amount {
  font-weight: 600;
  color: #059669;
}
.status {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  min-width: 80px;
  text-align: center;
}
.empty {
  color: #9ca3af;
  font-style: italic;
  text-align: center;
  padding: 2rem;
}
.transaction-item.selected {
  border-color: #2563eb;
  background: #eff6ff;
}
</style>
