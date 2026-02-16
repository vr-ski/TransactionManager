import apiClient from "./api";
import type {
  TransactionDetail,
  TransactionListResponse,
  TransactionCreateRequest,
  TransactionUpdateRequest,
} from "@/types/transactions";

export const transactionService = {
  async create(data: TransactionCreateRequest): Promise<TransactionDetail> {
    const response = await apiClient.post<TransactionDetail>(
      "/transactions/create",
      data,
    );
    return response.data;
  },

  async update(
    txId: number,
    data: TransactionUpdateRequest,
  ): Promise<TransactionDetail> {
    const response = await apiClient.patch<TransactionDetail>(
      `/transactions/${txId}`,
      data,
    );
    return response.data;
  },

  async getRecent(): Promise<TransactionListResponse> {
    const response = await apiClient.get<TransactionListResponse>(
      "/transactions/recent",
    );
    return response.data;
  },

  async getById(txId: number): Promise<TransactionDetail> {
    const response = await apiClient.get<TransactionDetail>(
      `/transactions/${txId}`,
    );
    return response.data;
  },
};
