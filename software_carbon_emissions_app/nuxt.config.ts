// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
sss: false,
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/globals.css'],
  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
        'chart.js'
      ]
    },
    server: {
      watch: {
        usePolling: true,
        interval: 1000
      },
      hmr: {
        protocol: 'ws',
        port: 3000
      }
    }
  }
})
