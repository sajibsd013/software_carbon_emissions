<template>
  <div v-if="!showResults"
    class="flex flex-col items-center justify-center min-h-[400px] p-8 text-center bg-gray-50 border border-dashed border-gray-300 rounded-2xl transition-all duration-300">
    <div class="flex items-center justify-center w-16 h-16 mb-4 bg-green-100 rounded-2xl ring-8 ring-green-50">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 3v18h18" />
        <path d="M18 9l-5 5-4-4-3 3" />
      </svg>
    </div>
    <h3 class="text-lg font-semibold text-gray-900 mb-1">No results yet</h3>
    <p class="text-sm text-gray-500 max-w-sm leading-relaxed">
      Fetch GitHub data or fill in the values manually, then calculate emissions to see your detailed breakdown here.
    </p>
  </div>

  <div v-else class="flex flex-col gap-6 animate-in fade-in duration-500">

    <div class="flex items-center justify-between">
      <h2 class="text-lg font-semibold text-gray-900">Emissions Report</h2>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="p-5 bg-white border border-gray-200 rounded-xl shadow-sm">
        <div class="text-sm font-medium text-gray-500 mb-1">Total Emissions</div>
        <div class="text-2xl font-bold text-gray-900">
          {{ results?.total_carbon_emissions_kgCO2eq?.toFixed(4) ?? '—' }} <span
            class="text-sm font-medium text-gray-400">kgCO₂eq</span>
        </div>
      </div>
      <div class="p-5 bg-amber-50 border border-amber-100 rounded-xl shadow-sm">
        <div class="text-sm font-medium text-amber-700 mb-1">Development</div>
        <div class="text-2xl font-bold text-amber-600">
          {{ results?.dev_phase_total_carbon_emissions_kgCO2eq?.toFixed(4) ?? '—' }} <span
            class="text-sm font-medium text-amber-400">kgCO₂eq</span>
        </div>
      </div>
      <div class="p-5 bg-blue-50 border border-blue-100 rounded-xl shadow-sm">
        <div class="text-sm font-medium text-blue-700 mb-1">Deployment</div>
        <div class="text-2xl font-bold text-blue-600">
          {{ results?.deploy_phase_total_carbon_emissions_kgCO2eq?.toFixed(4) ?? '—' }} <span
            class="text-sm font-medium text-blue-400">kgCO₂eq</span>
        </div>
      </div>
      <div class="p-5 bg-orange-50 border border-orange-100 rounded-xl shadow-sm">
        <div class="text-sm font-medium text-orange-700 mb-1">Usage</div>
        <div class="text-2xl font-bold text-orange-600">
          {{ results?.usage_phase_total_carbon_emissions_kgCO2eq?.toFixed(4) ?? '—' }} <span
            class="text-sm font-medium text-orange-400">kgCO₂eq</span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <div class="p-6 bg-white border border-gray-200 rounded-xl shadow-sm flex flex-col justify-between">
        <h3 class="text-sm font-semibold text-gray-900 mb-4">Phase Distribution</h3>

        <div class="relative flex items-center justify-center flex-grow py-4">
          <svg viewBox="0 0 100 100" class="w-64 h-64 transform -rotate-90">
            <circle cx="50" cy="50" r="40" fill="none" stroke="#f3f4f6" stroke-width="15" />

            <circle cx="50" cy="50" r="40" fill="none" stroke="#f97316" stroke-width="15"
              :stroke-dasharray="usageDasharray" class="transition-all duration-1000 ease-out" />

            <circle cx="50" cy="50" r="40" fill="none" stroke="#3b82f6" stroke-width="15"
              :stroke-dasharray="deployDasharray" :stroke-dashoffset="deployOffset"
              class="transition-all duration-1000 ease-out" />

            <circle cx="50" cy="50" r="40" fill="none" stroke="#f59e0b" stroke-width="15"
              :stroke-dasharray="devDasharray" :stroke-dashoffset="devOffset"
              class="transition-all duration-1000 ease-out" />
          </svg>
          <div class="absolute flex flex-col items-center justify-center text-center">
            <span class="text-xs text-gray-500 font-medium">Total</span>
            <span class="text-lg font-bold text-gray-900">{{ results?.total_carbon_emissions_kgCO2eq?.toFixed(1)
              }}</span>
          </div>
        </div>

        <div class="flex justify-center gap-6 mt-4">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-amber-500"></span>
            <span class="text-xs font-medium text-gray-600">Dev</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-blue-500"></span>
            <span class="text-xs font-medium text-gray-600">Deploy</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-orange-500"></span>
            <span class="text-xs font-medium text-gray-600">Usage</span>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-6">

        <div class="p-6 bg-white border border-gray-200 rounded-xl shadow-sm">
          <div class="space-y-5">
            <div>
              <div class="flex justify-between text-sm mb-1.5">
                <span class="font-medium text-gray-600">Development</span>
                <span class="font-bold text-amber-600">{{ devPct }}%</span>
              </div>
              <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                <div class="h-full bg-amber-500 rounded-full transition-all duration-1000"
                  :style="{ width: devPct + '%' }"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-sm mb-1.5">
                <span class="font-medium text-gray-600">Deployment</span>
                <span class="font-bold text-blue-600">{{ deployPct }}%</span>
              </div>
              <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full transition-all duration-1000"
                  :style="{ width: deployPct + '%' }"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-sm mb-1.5">
                <span class="font-medium text-gray-600">Usage</span>
                <span class="font-bold text-orange-600">{{ usagePct }}%</span>
              </div>
              <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                <div class="h-full bg-orange-500 rounded-full transition-all duration-1000"
                  :style="{ width: usagePct + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="p-6 bg-white border border-gray-200 rounded-xl shadow-sm">
          <h3 class="text-sm font-semibold text-gray-900 mb-4">Per-Unit Emissions</h3>
          <div class="divide-y divide-gray-100">
            <div class="flex justify-between py-2.5 first:pt-0 bg-purple-50/50 -mx-2 px-2 rounded-md mb-1">

              <span class="text-sm font-bold text-purple-700">
                SCI Score
              </span>
              <span class="text-sm font-medium text-purple-700 flex items-center gap-1.5">
                Functional Unit (R)
                <span class="cursor-help text-purple-400 text-xs"
                  title="Software Carbon Intensity (Emissions per Functional Unit)">ⓘ</span>
              </span>
            </div>
            <div class="flex justify-between py-2.5 last:pb-0">
              <span class="text-sm font-semibold text-gray-900">{{
                formatValue(results?.dev_phase_carbon_emissions_per_month_kgCO2eq) }}</span>
              <span class="text-sm text-gray-500">kgCO₂eq/month <span
                  class="text-[9px] uppercase font-medium text-purple-500">(Dev Phase)</span> </span>

            </div>
            <div class="flex justify-between py-2.5">
              <span class="text-sm font-semibold text-gray-900">{{
                formatValue(results?.dev_phase_carbon_emissions_per_commit_kgCO2eq) }}</span>
              <span class="text-sm text-gray-500">kgCO₂eq/Commit <span
                  class="text-[9px] uppercase font-medium text-purple-500">(Dev Phase)</span> </span>

            </div>
            <div class="flex justify-between py-2.5">
              <span class="text-sm font-semibold text-gray-900">{{
                formatValue(results?.dev_phase_carbon_emissions_per_ci_kgCO2eq) }}</span>
              <span class="text-sm text-gray-500">kgCO₂eq/CI Run <span
                  class="text-[9px] uppercase font-medium text-purple-500">(Dev Phase)</span> </span>

            </div>
            <div class="flex justify-between py-2.5">
              <span class="text-sm font-semibold text-gray-900">{{
                formatValue(results?.deploy_phase_carbon_emissions_per_release_kgCO2eq) }}</span>
              <span class="text-sm text-gray-500">kgCO₂eq/Release <span
                  class="text-[9px] uppercase font-medium text-purple-500">(Deploy Phase)</span> </span>

            </div>
            <div class="flex justify-between py-2.5">
              <span class="text-sm font-semibold text-gray-900">{{
                formatValue(results?.usage_phase_carbon_emissions_per_user_kgCO2eq) }}</span>
              <span class="text-sm text-gray-500">kgCO₂eq/User <span
                  class="text-[9px] uppercase font-medium text-purple-500">(Usage Phase)</span> </span>

            </div>
          </div>
        </div>

      </div>
    </div>

    <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden w-full max-w-4xl mx-auto">
      <div class="p-5 border-b border-gray-100 bg-gray-50/50">
        <h3 class="text-sm font-semibold text-gray-900">Detailed Breakdown</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-white border-b border-gray-100">
              <th class="py-3 px-5 text-xs font-medium text-gray-400 uppercase tracking-wider">Metric</th>
              <th class="py-3 px-5 text-xs font-medium text-gray-400 tracking-wider text-right">Emissions
                (kgCO₂eq)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50">
            <tr v-for="row in breakdownRows" :key="row.label" class="hover:bg-gray-50/50 transition-colors">
              <td class="py-3 px-5 text-sm" :class="row.bold ? 'font-semibold text-gray-900' : 'text-gray-600'">
                <span class="inline-block w-2.5 h-2.5 rounded-full mr-2.5"
                  :style="{ backgroundColor: row.color }"></span>
                {{ row.label }}
              </td>
              <td class="py-3 px-5 text-sm text-right tabular-nums"
                :class="row.bold ? 'font-bold text-gray-900' : 'font-medium'"
                :style="{ color: !row.bold ? row.color : '' }">
                {{ row.val?.toFixed(6) ?? '—' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  results: {
    type: Object,
    default: null
  },
  repoLabel: {
    type: String,
    default: 'Manual Entry'
  }
});

const showResults = computed(() => !!props.results);

// --- Percentages ---
const devPct = computed(() => {
  if (!props.results || !props.results.total_carbon_emissions_kgCO2eq) return '0.0';
  return ((props.results.dev_phase_total_carbon_emissions_kgCO2eq / props.results.total_carbon_emissions_kgCO2eq) * 100).toFixed(5);
});

const deployPct = computed(() => {
  if (!props.results || !props.results.total_carbon_emissions_kgCO2eq) return '0.0';
  return ((props.results.deploy_phase_total_carbon_emissions_kgCO2eq / props.results.total_carbon_emissions_kgCO2eq) * 100).toFixed(5);
});

const usagePct = computed(() => {
  if (!props.results || !props.results.total_carbon_emissions_kgCO2eq) return '0.0';
  return ((props.results.usage_phase_total_carbon_emissions_kgCO2eq / props.results.total_carbon_emissions_kgCO2eq) * 100).toFixed(5);
});


// --- SVG Donut Chart Logic ---
// Circumference of a circle with r=40 is 2 * PI * 40 = 251.327
const CIRCUMFERENCE = 251.327;

// Raw Numbers (0 to 1)
const devRatio = computed(() => parseFloat(devPct.value) / 100 || 0);
const deployRatio = computed(() => parseFloat(deployPct.value) / 100 || 0);
const usageRatio = computed(() => parseFloat(usagePct.value) / 100 || 0);

// Dasharrays (How long the stroke is)
const devDasharray = computed(() => `${devRatio.value * CIRCUMFERENCE} ${CIRCUMFERENCE}`);
const deployDasharray = computed(() => `${deployRatio.value * CIRCUMFERENCE} ${CIRCUMFERENCE}`);
const usageDasharray = computed(() => `${usageRatio.value * CIRCUMFERENCE} ${CIRCUMFERENCE}`);

// Offsets (Where the stroke starts, moving backwards)
// Development starts at 0
const devOffset = computed(() => 0);
// Deployment starts after Development
const deployOffset = computed(() => -(devRatio.value * CIRCUMFERENCE));
// We don't strictly need an offset for Usage because we layered it at the bottom of the SVG in the HTML, 
// but mathematically it would start after Dev + Deploy.


// --- Table Data ---
const breakdownRows = computed(() => {
  if (!props.results) return [];
  return [
    { label: 'Development Phase — per month', val: props.results.dev_phase_carbon_emissions_per_month_kgCO2eq, color: '#f59e0b' },
    { label: 'Development Phase — per commit', val: props.results.dev_phase_carbon_emissions_per_commit_kgCO2eq, color: '#f59e0b' },
    { label: 'Development Phase — per CI run', val: props.results.dev_phase_carbon_emissions_per_ci_kgCO2eq, color: '#f59e0b' },
    { label: 'Development Phase — total', val: props.results.dev_phase_total_carbon_emissions_kgCO2eq, color: '#d97706', bold: true },
    { label: 'Deployment Phase — per release', val: props.results.deploy_phase_carbon_emissions_per_release_kgCO2eq, color: '#3b82f6' },
    { label: 'Deployment Phase — total', val: props.results.deploy_phase_total_carbon_emissions_kgCO2eq, color: '#2563eb', bold: true },
    { label: 'Usage Phase — per month', val: props.results.usage_phase_carbon_emissions_per_month_kgCO2eq, color: '#f97316' },
    { label: 'Usage Phase — per user', val: props.results.usage_phase_carbon_emissions_per_user_kgCO2eq, color: '#f97316' },
    { label: 'Usage Phase — total', val: props.results.usage_phase_total_carbon_emissions_kgCO2eq, color: '#ea580c', bold: true },
    { label: 'TOTAL CARBON EMISSIONS', val: props.results.total_carbon_emissions_kgCO2eq, color: '#16a34a', bold: true }
  ];
});

const formatValue = (val: number | null | undefined) => {
  return val == null ? '—' : val.toFixed(4);
};
</script>