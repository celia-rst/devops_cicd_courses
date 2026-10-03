import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:5173", // <-- URL du frontend Vite
    setupNodeEvents() {
      // implement node event listeners here
      // Événements Node (non utilisés ici)
    },
  },
});
