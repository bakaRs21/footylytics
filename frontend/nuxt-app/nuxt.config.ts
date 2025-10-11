// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from "nuxt/config"

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxt/icon'],
  ssr: true,
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE
    }
  },
  vite: {
    server: {
      proxy: {
        "/api" : {
          target: process.env.API_BASE || "http://localhost:8000",
          changeOrigin: true,
          secure: false,
        } 
      }
    }
  }
})