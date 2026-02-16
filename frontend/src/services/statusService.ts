import apiClient from "./api";

export interface Status {
  status_id: number;
  code: string;
  display_name: string;
  color: string;
}

export const statusService = {
  async getAll(): Promise<Status[]> {
    const response = await apiClient.get<Status[]>("/statuses");
    return response.data;
  },
};
