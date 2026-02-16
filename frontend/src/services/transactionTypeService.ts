import apiClient from "./api";

export interface TransactionType {
  transaction_type_id: number;
  code: string;
  display_name: string;
}

export const transactionTypeService = {
  async getAll(): Promise<TransactionType[]> {
    const response =
      await apiClient.get<TransactionType[]>("/transaction-types");
    return response.data;
  },
};
