export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/globals.css'],

  future: {
    compatibilityVersion: 4,
  },

  nitro: {
    preset: 'node-server'
  }
})