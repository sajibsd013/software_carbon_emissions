<template>
  <div class="min-h-screen bg-[#f5f7f5]">
    <main class="max-w-7xl mx-auto px-6 py-7">
      <!-- Page heading -->
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-[#1a2e1a] mb-1">Software Carbon Footprint Analyzer</h2>
        <p class="text-sm text-[#6b7c6b]">Measure development, deployment, and usage phase emissions from GitHub or manual data.</p>
      </div>
      <Emission/>
    </main>
    <Toast ref="toastRef" />
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false,

});
useHead({
  title: 'Software Carbon Emissions Calculator',
  meta: [
    { name: 'description', content: 'Calculate the carbon footprint of your software projects based on GitHub data or manual inputs.' }
  ]
});





</script>

