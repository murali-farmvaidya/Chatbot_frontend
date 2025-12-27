import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  server: {
    port: process.env.PORT || 5173,
    host: "0.0.0.0",
    allowedHosts: [
      ".onrender.com" // allow all Render subdomains
    ]
  },

  preview: {
    port: process.env.PORT || 5173,
    host: "0.0.0.0",
    allowedHosts: [
      ".onrender.com"
    ]
  }
});
