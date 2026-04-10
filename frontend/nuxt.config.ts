import { defineNuxtConfig } from "nuxt/config";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [ '@nuxtjs/i18n' ],
  components: [
    { 
      path: "~/components",
      pathPrefix: false,
    }
  ],
  css: [
    "~/assets/css/main.css", "~/assets/css/typography.css", "~/assets/css/layouts.css", 
    "~/assets/css/utilities.css", "~/assets/css/cards.css", "~/assets/css/forms.css",
    "~/assets/css/badges.css", "~/assets/css/buttons.css",
    "~/assets/css/compare.css", "~/assets/css/dropdowns.css"
  ], 
  plugins: [
    { src: "~/plugins/apexcharts.client.ts", mode: "client" },
  ],
  i18n: {
    defaultLocale: 'en',
    locales: [
      { code: 'en', name: 'English', language: 'en-US', file: 'en.json' },
      { code: 'cs', name: 'Čeština', language: 'cs-CZ', file: 'cs.json' },
    ],
    skipSettingLocaleOnNavigate: false,
  },
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
  },
})