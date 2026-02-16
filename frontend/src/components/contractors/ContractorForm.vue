<template>
  <div class="contractor-form">
    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="name">Name</label>
        <input id="name" v-model="form.name" required />
      </div>
      <div class="actions">
        <button type="submit" class="save-btn">Create</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { ContractorCreate } from "@/types/contractor";

const emit = defineEmits<{ (e: "save", data: ContractorCreate): void }>();
const form = ref<ContractorCreate>({ name: "" });

function onSubmit() {
  emit("save", form.value);
  form.value = { name: "" }; // reset
}
</script>

<style scoped>
.contractor-form {
  background: transparent;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 500;
  color: #4b5563;
}
.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}
.actions {
  margin-top: 1.5rem;
}
.save-btn {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
}
</style>
