import { defineStore } from "pinia";
import { ref } from "vue";
import { contractorService } from "@/services/contractorService";
import type { Contractor, ContractorCreate } from "@/types/contractor";

export const useContractorStore = defineStore("contractors", () => {
  const contractors = ref<Contractor[]>([]);
  const currentContractor = ref<Contractor | null>(null);

  async function fetchContractors(userId: number) {
    contractors.value = await contractorService.getByUser(userId);
  }

  async function fetchContractor(id: number) {
    currentContractor.value = await contractorService.getById(id);
  }

  async function createContractor(userId: number, payload: ContractorCreate) {
    const newContractor = await contractorService.createForUser(
      userId,
      payload,
    );
    contractors.value.push(newContractor);
    return newContractor;
  }

  return {
    contractors,
    currentContractor,
    fetchContractors,
    fetchContractor,
    createContractor,
  };
});
