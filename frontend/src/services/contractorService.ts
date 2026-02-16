import apiClient from "./api";
import type { Contractor, ContractorCreate } from "@/types/contractor";

export const contractorService = {
  async getByUser(userId: number): Promise<Contractor[]> {
    const response = await apiClient.get<Contractor[]>(
      `/contractors/user/${userId}`,
    );
    return response.data;
  },

  async getById(contractorId: number): Promise<Contractor> {
    const response = await apiClient.get<Contractor>(
      `/contractors/${contractorId}`,
    );
    return response.data;
  },

  async createForUser(
    userId: number,
    data: ContractorCreate,
  ): Promise<Contractor> {
    const response = await apiClient.post<Contractor>(
      `/contractors/user/${userId}`,
      data,
    );
    return response.data;
  },
};
