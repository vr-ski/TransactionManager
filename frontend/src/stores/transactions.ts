import { defineStore } from "pinia";
import { ref } from "vue";
import { transactionService } from "@/services/transactionService";
import type {
  TransactionDetail,
  TransactionListItem,
  TransactionCreateRequest,
  TransactionUpdateRequest,
} from "@/types/transactions";

export const useTransactionStore = defineStore("transactions", () => {
  const recentTransactions = ref<TransactionListItem[]>([]);
  const currentTransaction = ref<TransactionDetail | null>(null);

  async function fetchRecent() {
    const response = await transactionService.getRecent();
    recentTransactions.value = response.items;
  }

  async function fetchTransaction(id: number) {
    currentTransaction.value = await transactionService.getById(id);
  }

  async function createTransaction(payload: TransactionCreateRequest) {
    const newTx = await transactionService.create(payload);
    // Transform the detail response to a list item
    const listItem: TransactionListItem = {
      transaction_id: newTx.transaction_id,
      contractor_from: newTx.contractor_from,
      contractor_to: newTx.contractor_to,
      amount: newTx.amount,
      transaction_type: newTx.transaction_type.display_name,
      status: newTx.status,
      created_at: newTx.created_at,
    };
    recentTransactions.value = [listItem, ...recentTransactions.value];
    return newTx;
  }

  async function updateTransaction(
    id: number,
    payload: TransactionUpdateRequest,
  ) {
    const updated = await transactionService.update(id, payload);
    if (currentTransaction.value?.transaction_id === id) {
      currentTransaction.value = updated;
    }
    const index = recentTransactions.value.findIndex(
      (tx: TransactionListItem) => tx.transaction_id === id,
    );
    if (index !== -1) {
      // Transform the updated detail to a list item
      const listItem: TransactionListItem = {
        transaction_id: updated.transaction_id,
        contractor_from: updated.contractor_from,
        contractor_to: updated.contractor_to,
        amount: updated.amount,
        transaction_type: updated.transaction_type.display_name,
        status: updated.status,
        created_at: updated.created_at,
      };
      recentTransactions.value[index] = listItem;
    }
    return updated;
  }

  return {
    recentTransactions,
    currentTransaction,
    fetchRecent,
    fetchTransaction,
    createTransaction,
    updateTransaction,
  };
});
