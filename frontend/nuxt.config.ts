import { defineNuxtConfig } from "nuxt/config";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss"],
  components: [
    { 
      path: "~/components",
      pathPrefix: false,
    }
  ],
  css: ["~/assets/css/tailwind.css"],
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
    },
  }
})
