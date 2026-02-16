import apiClient from "./api";

export const healthService = {
  async checkHealth(): Promise<{ status: string }> {
    const response = await apiClient.get("/health");
    return response.data;
  },
};
