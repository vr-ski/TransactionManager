<template>
  <div>
    <h2 class="section-header">Recent Transactions</h2>

    <!-- Search and Sort Controls -->
    <div class="controls">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search..."
        :title="'Search by contractor, amount, status, type, or date'"
        class="search-input"
      />
      <div class="sort-buttons">
        <button
          v-for="option in sortOptions"
          :key="option.value"
          class="sort-btn"
          :class="{ active: sortBy === option.value }"
          @click="handleSortClick(option.value)"
        >
          {{ option.label }}
          <span v-if="sortBy === option.value" class="sort-arrow">
            {{ sortDirection === "asc" ? "↑" : "↓" }}
          </span>
        </button>
      </div>
    </div>

    <TransactionList
      :transactions="filteredAndSortedTransactions"
      @select="goToDetail"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { useTransactionStore } from "@/stores/transactions";
import TransactionList from "@/components/transactions/TransactionList.vue";
import { useRouter } from "vue-router";

const transactionStore = useTransactionStore();
const router = useRouter();

const searchQuery = ref("");
const sortBy = ref("date");
const sortDirection = ref<"asc" | "desc">("desc"); // default for date

const sortOptions = [
  { value: "date", label: "Date" },
  { value: "contractor_from", label: "From" },
  { value: "contractor_to", label: "To" },
  { value: "amount", label: "Amount" },
];

function handleSortClick(value: string) {
  if (sortBy.value === value) {
    // Toggle direction
    sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
  } else {
    sortBy.value = value;
    // Set default direction
    sortDirection.value = value === "date" ? "desc" : "asc";
  }
}

// Helper for date search
function getDateSearchString(dateStr: string): string {
  try {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return "";
    const month = date
      .toLocaleDateString(undefined, { month: "short" })
      .toLowerCase();
    const day = date.getDate();
    const year = date.getFullYear();
    const iso = date.toISOString().split("T")[0];
    const monthNum = (date.getMonth() + 1).toString().padStart(2, "0");
    return `${month} ${day} ${year} ${iso} ${monthNum}`;
  } catch {
    return "";
  }
}

const filteredAndSortedTransactions = computed(() => {
  // Start with the raw transactions from the store
  let filtered = [...transactionStore.recentTransactions];

  // Apply search filter if query exists
  const query = searchQuery.value.toLowerCase().trim();
  if (query) {
    filtered = filtered.filter((tx) => {
      const dateString = getDateSearchString(tx.created_at);
      return (
        tx.contractor_from.toLowerCase().includes(query) ||
        tx.contractor_to.toLowerCase().includes(query) ||
        tx.amount.toString().includes(query) ||
        tx.status.display_name.toLowerCase().includes(query) ||
        tx.transaction_type.toLowerCase().includes(query) ||
        dateString.includes(query)
      );
    });
  }

  // Apply sorting
  filtered.sort((a, b) => {
    let comparison = 0;
    switch (sortBy.value) {
      case "contractor_from":
        comparison = a.contractor_from.localeCompare(b.contractor_from);
        break;
      case "contractor_to":
        comparison = a.contractor_to.localeCompare(b.contractor_to);
        break;
      case "amount":
        comparison = a.amount - b.amount;
        break;
      case "date":
      default:
        comparison =
          new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
        break;
    }
    return sortDirection.value === "asc" ? comparison : -comparison;
  });

  return filtered;
});

function goToDetail(id: number) {
  router.push(`/transactions/${id}`);
}

onMounted(() => {
  transactionStore.fetchRecent();
});
</script>

<style scoped>
.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
}
.search-input {
  flex: 2;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}
.search-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}
.sort-buttons {
  display: flex;
  gap: 0.5rem;
}
.sort-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.sort-btn:hover {
  background: #f3f4f6;
}
.sort-btn.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}
.sort-arrow {
  font-size: 0.875rem;
  line-height: 1;
}
</style>
