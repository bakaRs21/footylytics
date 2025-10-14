// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from "nuxt/config"

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxt/icon', "@nuxtjs/tailwindcss"],
  ssr: true,
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE,
    }
  },
  vite: {
    server: {
      proxy: {
        "/api" : {
          target: process.env.NUXT_PUBLIC_API_BASE,
          changeOrigin: true,
          secure: false,
        } 
      }
    }
  }
})