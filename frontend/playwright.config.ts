import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e", // only run tests in the e2e folder
  use: {
    baseURL: "http://localhost:5173",
  },
});
