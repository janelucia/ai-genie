/// <reference types="vitest/config" />
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  test: {
    environment: "jsdom",
  },
  server: {
    port: 3000,
    host: true, // <--- Allow all hosts (necessary for ngrok to tunnel into dev server)
    strictPort: true, // Don't switch port if 3000 is busy (optional but nice for consistency)
    allowedHosts: [
      "participants-analysis-interval-developments.trycloudflare.com",  // Allow ngrok frontend URL
    ],
  },
});
