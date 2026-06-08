<template>
  <!-- Minimalist Empty State -->
<div v-if="!showResults"
     class="flex flex-col items-center justify-center min-h-[450px] p-6 sm:p-12 text-center bg-gray-50/40 border border-gray-200/80 rounded-2xl transition-all duration-300 font-formal-sans max-w-2xl mx-auto my-4">

  <!-- Updated Icon: Professional Data/Audit Ledger Symbol (Removed Dollar Symbol) -->
  <div class="flex items-center justify-center w-12 h-12 mb-4 bg-emerald-50 border border-emerald-100 rounded-xl">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#047857" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
      <polyline points="14 2 14 8 20 8"></polyline>
      <line x1="16" y1="13" x2="8" y2="13"></line>
      <line x1="16" y1="17" x2="8" y2="17"></line>
      <polyline points="10 9 9 9 8 9"></polyline>
    </svg>
  </div>

  <!-- Heading -->
  <h3 class="text-lg font-semibold text-gray-900 tracking-tight mb-2 font-formal-serif">
    Environmental Ledger Ready for Input
  </h3>

  <!-- Context Description -->
  <p class="text-sm text-gray-500 max-w-md leading-relaxed mb-8">
    To compute the Software Carbon Intensity (SCI) index and generate your compliance statement, follow the configuration steps below.
  </p>

  <!-- Step-by-Step Instructions Matrix -->
  <div class="w-full grid grid-cols-1 sm:grid-cols-2 gap-4 text-left border-t border-gray-250/60 pt-6">

    <!-- Option 1: Automated Integration -->
    <div class="p-4 bg-white border border-gray-200 rounded-xl shadow-sm hover:border-gray-300 transition-colors">
      <div class="flex items-center gap-2 mb-2">
        <span class="flex items-center justify-center w-5 h-5 rounded-full bg-emerald-600 text-white font-mono text-[11px] font-bold">1</span>
        <h4 class="text-xs font-bold uppercase tracking-wider text-gray-700">Automated Audit</h4>
      </div>
      <p class="text-xs text-gray-500 leading-relaxed">
        Provide a valid GitHub repository URL. The system will automatically compile active development weeks, total commit registry, and integration pipeline runs.
      </p>
    </div>

    <!-- Option 2: Manual Parameters -->
    <div class="p-4 bg-white border border-gray-200 rounded-xl shadow-sm hover:border-gray-300 transition-colors">
      <div class="flex items-center gap-2 mb-2">
        <span class="flex items-center justify-center w-5 h-5 rounded-full bg-emerald-600 text-white font-mono text-[11px] font-bold">2</span>
        <h4 class="text-xs font-bold uppercase tracking-wider text-gray-700">Manual Entry</h4>
      </div>
      <p class="text-xs text-gray-500 leading-relaxed">
        Enter operational variables directly including cloud server power profile, localized grid carbon coefficients, and structural user base counts.
      </p>
    </div>

  </div>

  <!-- Bottom CTA Action Hint -->
  <div class="mt-6 flex items-center gap-2 text-xs text-emerald-800 bg-emerald-50/80 px-3 py-1.5 rounded-lg border border-emerald-100">
    <span>Fill the form controls above and trigger <strong>"Calculate Emissions"</strong> to render dashboard analytics.</span>
  </div>

</div>

  <!-- Main Carbon Dashboard -->
  <div v-else class="flex flex-col gap-6 sm:gap-8 animate-in fade-in duration-500 font-formal-sans text-gray-900">

    <!-- Formal Document Header -->
    <div class="flex flex-col sm:flex-row sm:items-baseline justify-between border-b border-gray-200 pb-4 gap-2">
      <div>
        <h2 class="text-xs sm:text-sm font-bold tracking-widest uppercase text-gray-400 font-formal-sans">Carbon
          Accounting Statement</h2>
        <p class="text-sm font-mono text-gray-600 mt-1">{{ repoLabel }}</p>
      </div>
      <span class="text-xs text-gray-500 italic font-formal-serif">Unit of Measure: Kilograms of CO₂ Equivalent (kgCO₂eq)</span>
    </div>

    <!-- Core Impact Ledger Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Total Emissions -->
      <div class="p-6 bg-emerald-50/80 border border-emerald-200 rounded-xl shadow-sm flex flex-col justify-between">
        <span
            class="text-sm font-bold tracking-wider text-emerald-800 uppercase font-formal-sans">Total Emissions</span>
        <div class="mt-4">
          <span
              class="text-3xl sm:text-4xl font-semibold tracking-tight text-emerald-950 font-formal-serif block truncate">
            {{ results?.total_carbon_emissions_kgCO2eq?.toFixed(4) ?? '—' }}
          </span>
          <span class="text-[10px] sm:text-xs font-semibold text-emerald-700 uppercase tracking-widest block mt-1">Combined Footprint</span>
        </div>
      </div>
      <!-- Dev -->
      <div class="p-6 bg-amber-50/80 border border-amber-200 rounded-xl shadow-sm flex flex-col justify-between">
        <span class="text-sm font-bold tracking-wider text-amber-800 uppercase font-formal-sans">01 / Development</span>
        <div class="mt-4">
          <span class="text-2xl sm:text-3xl font-semibold text-amber-950 font-formal-serif block truncate">
            {{ results?.dev_phase_total_carbon_emissions_kgCO2eq?.toFixed(4) ?? '—' }}
          </span>
          <span class="text-[10px] sm:text-xs font-bold text-amber-700 uppercase tracking-widest block mt-1">
            Share: {{ devPct }}%
          </span>
        </div>
      </div>
      <!-- Deploy -->
      <div class="p-6 bg-blue-50/80 border border-blue-200 rounded-xl shadow-sm flex flex-col justify-between">
        <span class="text-sm font-bold tracking-wider text-blue-800 uppercase font-formal-sans">02 / Deployment</span>
        <div class="mt-4">
          <span class="text-2xl sm:text-3xl font-semibold text-blue-950 font-formal-serif block truncate">
            {{ results?.deploy_phase_total_carbon_emissions_kgCO2eq?.toFixed(4) ?? '—' }}
          </span>
          <span class="text-[10px] sm:text-xs font-bold text-blue-700 uppercase tracking-widest block mt-1">
            Share: {{ deployPct }}%
          </span>
        </div>
      </div>
      <!-- Usage -->
      <div class="p-6 bg-orange-50/80 border border-orange-200 rounded-xl shadow-sm flex flex-col justify-between">
        <span
            class="text-sm font-bold tracking-wider text-orange-800 uppercase font-formal-sans">03 / Production Usage</span>
        <div class="mt-4">
          <span class="text-2xl sm:text-3xl font-semibold text-orange-950 font-formal-serif block truncate">
            {{ results?.usage_phase_total_carbon_emissions_kgCO2eq?.toFixed(4) ?? '—' }}
          </span>
          <span class="text-[10px] sm:text-xs font-bold text-orange-700 uppercase tracking-widest block mt-1">
            Share: {{ usagePct }}%
          </span>
        </div>
      </div>
    </div>

    <!-- Graphical Breakdown & Normalized Metrics -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 items-stretch">

      <!-- Phase Distribution Gauge (5 Columns) -->
      <div
          class="lg:col-span-5 p-6 bg-white border border-gray-200 rounded-xl shadow-sm flex flex-col items-center justify-between">
        <div class="w-full flex justify-between items-center mb-4">
          <h3 class="text-sm font-bold uppercase tracking-wider text-gray-500 font-formal-sans">Proportional Share</h3>
          <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">Visualized</span>
        </div>

        <div class="relative flex items-center justify-center w-full max-w-[210px] aspect-square py-2">
          <svg viewBox="0 0 100 100" class="w-full h-full transform -rotate-90">
            <circle cx="50" cy="50" r="42" fill="none" stroke="#f4f4f5" stroke-width="10"/>
            <!-- Segment Dev -->
            <circle cx="50" cy="50" r="42" fill="none" stroke="#f59e0b" stroke-width="10"
                    :stroke-dasharray="devDasharray" stroke-dashoffset="0"
                    class="transition-all duration-1000 ease-out"/>
            <!-- Segment Deploy -->
            <circle cx="50" cy="50" r="42" fill="none" stroke="#3b82f6" stroke-width="10"
                    :stroke-dasharray="deployDasharray" :stroke-dashoffset="deployOffset"
                    class="transition-all duration-1000 ease-out"/>
            <!-- Segment Usage -->
            <circle cx="50" cy="50" r="42" fill="none" stroke="#f97316" stroke-width="10"
                    :stroke-dasharray="usageDasharray" :stroke-dashoffset="usageOffset"
                    class="transition-all duration-1000 ease-out"/>
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span
                class="text-[10px] font-bold text-gray-400 uppercase tracking-widest font-formal-sans">Aggregate</span>
            <span class="text-2xl font-bold text-gray-900 mt-0.5 font-formal-serif">
              {{ results?.total_carbon_emissions_kgCO2eq?.toFixed(2) }}
            </span>
          </div>
        </div>

        <!-- Metric Bars -->
        <div class="w-full space-y-4 mt-6 pt-4 border-t border-gray-100">
          <div>
            <div class="flex justify-between text-xs mb-1 text-gray-500">
              <span class="font-medium">Development Phase</span>
              <span class="font-bold text-gray-900">{{ devPct }}%</span>
            </div>
            <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
              <div class="h-full bg-amber-500 transition-all duration-1000" :style="{ width: devPct + '%' }"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between text-xs mb-1 text-gray-500">
              <span class="font-medium">Deployment Phase</span>
              <span class="font-bold text-gray-900">{{ deployPct }}%</span>
            </div>
            <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
              <div class="h-full bg-blue-500 transition-all duration-1000" :style="{ width: deployPct + '%' }"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between text-xs mb-1 text-gray-500">
              <span class="font-medium">Production Usage Phase</span>
              <span class="font-bold text-gray-900">{{ usagePct }}%</span>
            </div>
            <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
              <div class="h-full bg-orange-500 transition-all duration-1000" :style="{ width: usagePct + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Normalized SCI Indexes & Formulas (7 Columns) -->
      <div class="lg:col-span-7 p-6 bg-white border border-gray-200 rounded-xl shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex flex-col border-b border-gray-100 pb-4 mb-4">
            <h3 class="text-sm font-bold text-gray-900 uppercase tracking-wider font-formal-sans">Software Carbon
              Intensity Index</h3>
            <p class="text-xs text-gray-500 mt-1">Calculated carbon impact normalized against functional software
              metrics (R)</p>

            <!-- Standardized SCI Equation Block -->
            <div
                class="mt-4 p-4 bg-zinc-50 border border-zinc-200 rounded-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div
                  class="font-mono text-base font-bold text-zinc-900 bg-white px-3 py-1.5 rounded border border-zinc-300/60 shadow-sm self-center">
                SCI = <span class="text-emerald-700">(E × I) + M</span> / <span class="text-purple-700">R</span>
              </div>
              <div class="text-[11px] text-zinc-600 space-y-0.5 leading-relaxed">
                <div><span class="font-semibold text-zinc-900">E</span> = Energy consumed by the system</div>
                <div><span class="font-semibold text-zinc-900">I</span> = Regional grid carbon intensity coefficient
                </div>
                <div><span class="font-semibold text-zinc-900">M</span> = Embodied hardware operational lifecycle
                  emissions
                </div>
                <div><span class="font-semibold text-purple-700">R</span> = Functional Unit <span
                    class="italic text-zinc-400">(e.g., Per user, commit, month)</span></div>
              </div>
            </div>
          </div>

          <div class="divide-y divide-gray-150 text-sm">
            <div class="flex justify-between items-center py-3.5">
              <span class="text-gray-600 font-medium">Emissions / Operating Month <span
                  class="text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded ml-1.5">DEV</span></span>
              <span class="font-semibold text-gray-900 font-formal-serif text-base">{{
                  formatValue(results?.dev_phase_carbon_emissions_per_month_kgCO2eq)
                }}</span>
            </div>
            <div class="flex justify-between items-center py-3.5">
              <span class="text-gray-600 font-medium">Emissions / Repository Commit <span
                  class="text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded ml-1.5">DEV</span></span>
              <span class="font-semibold text-gray-900 font-formal-serif text-base">{{
                  formatValue(results?.dev_phase_carbon_emissions_per_commit_kgCO2eq)
                }}</span>
            </div>
            <div class="flex justify-between items-center py-3.5">
              <span class="text-gray-600 font-medium">Emissions / Pipeline CI Execution <span
                  class="text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded ml-1.5">DEV</span></span>
              <span class="font-semibold text-gray-900 font-formal-serif text-base">{{
                  formatValue(results?.dev_phase_carbon_emissions_per_ci_kgCO2eq)
                }}</span>
            </div>
            <div class="flex justify-between items-center py-3.5">
              <span class="text-gray-600 font-medium">Emissions / Deployment Release <span
                  class="text-[10px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded ml-1.5">DEPLOY</span></span>
              <span class="font-semibold text-gray-900 font-formal-serif text-base">{{
                  formatValue(results?.deploy_phase_carbon_emissions_per_release_kgCO2eq)
                }}</span>
            </div>
            <div class="flex justify-between items-center py-3.5">
              <span class="text-gray-600 font-medium">Emissions / Active System User <span
                  class="text-[10px] font-bold text-orange-700 bg-orange-50 px-2 py-0.5 rounded ml-1.5">USAGE</span></span>
              <span class="font-semibold text-gray-900 font-formal-serif text-base">{{
                  formatValue(results?.usage_phase_carbon_emissions_per_user_kgCO2eq)
                }}</span>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t border-gray-150 text-xs text-gray-400 italic">
          * Standard functional normalization enables structural green-software auditing under standard benchmarking.
        </div>
      </div>
    </div>

    <!-- Auditable Detailed Structural Ledger Redesign -->
    <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden w-full">
      <div
          class="p-5 border-b border-gray-150 bg-gray-50/50 flex flex-col sm:flex-row justify-between sm:items-center gap-1">
        <div>
          <h3 class="text-sm font-bold uppercase tracking-wider text-gray-900 font-formal-sans">Detailed Structural
            Carbon Ledger</h3>
          <!--          <p class="text-xs text-gray-500 mt-1">Formal ledger records structured by development cycles and production environments</p>-->
        </div>
        <span class="text-xs text-gray-400 font-mono tracking-wider self-start sm:self-center"></span>
      </div>
      <div class="overflow-x-auto w-full">
<table class="w-full text-left border-collapse min-w-[700px] text-sm font-formal-sans">
  <thead>
    <tr class="bg-zinc-50 border-b border-zinc-200 text-zinc-400 uppercase tracking-widest text-[10px] font-bold">
      <th class="py-4 px-6">Accounting Metric Layer</th>
      <th class="py-4 px-6 text-right">Raw Value (kgCO₂eq)</th>
    </tr>
  </thead>

  <tbody class="divide-y divide-zinc-100">
    <tr class="bg-zinc-50/70 border-y border-zinc-200/60">
      <td colspan="2" class="py-3 px-6 font-bold text-zinc-500 uppercase tracking-wider text-[10px]">
        01. Development Environment Sub-Metrics
      </td>
    </tr>
    <tr class="hover:bg-zinc-50/40 transition-colors">
      <td class="py-3.5 px-6 pl-10 text-zinc-600 flex items-center gap-2.5">
        <span class="w-2 h-2 rounded-full bg-amber-500"></span>
        Development Phase — per month
      </td>
      <td class="py-3.5 px-6 text-right font-mono text-zinc-900 font-medium text-base">
        {{ results?.dev_phase_carbon_emissions_per_month_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>
    <tr class="hover:bg-zinc-50/40 transition-colors">
      <td class="py-3.5 px-6 pl-10 text-zinc-600 flex items-center gap-2.5">
        <span class="w-2 h-2 rounded-full bg-amber-500"></span>
        Development Phase — per commit
      </td>
      <td class="py-3.5 px-6 text-right font-mono text-zinc-900 font-medium text-base">
        {{ results?.dev_phase_carbon_emissions_per_commit_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>
    <tr class="hover:bg-zinc-50/40 transition-colors">
      <td class="py-3.5 px-6 pl-10 text-zinc-600 flex items-center gap-2.5">
        <span class="w-2 h-2 rounded-full bg-amber-500"></span>
        Development Phase — per CI execution
      </td>
      <td class="py-3.5 px-6 text-right font-mono text-zinc-900 font-medium text-base">
        {{ results?.dev_phase_carbon_emissions_per_ci_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>
    <tr class="bg-amber-50/40 font-semibold border-b border-zinc-200">
      <td class="py-3.5 px-6 pl-10 text-amber-900">
        Development Phase — Total cumulative footprint
      </td>
      <td class="py-3.5 px-6 text-right font-mono text-amber-800 text-base">
        {{ results?.dev_phase_total_carbon_emissions_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>

    <tr class="bg-zinc-50/70 border-y border-zinc-200/60">
      <td colspan="2" class="py-3 px-6 font-bold text-zinc-500 uppercase tracking-wider text-[10px]">
        02. Deployment Pipeline Sub-Metrics
      </td>
    </tr>
    <tr class="hover:bg-zinc-50/40 transition-colors">
      <td class="py-3.5 px-6 pl-10 text-zinc-600 flex items-center gap-2.5">
        <span class="w-2 h-2 rounded-full bg-blue-500"></span>
        Deployment Phase — per release
      </td>
      <td class="py-3.5 px-6 text-right font-mono text-zinc-900 font-medium text-base">
        {{ results?.deploy_phase_carbon_emissions_per_release_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>
    <tr class="bg-blue-50/40 font-semibold border-b border-zinc-200">
      <td class="py-3.5 px-6 pl-10 text-blue-900">
        Deployment Phase — Total cumulative footprint
      </td>
      <td class="py-3.5 px-6 text-right font-mono text-blue-800 text-base">
        {{ results?.deploy_phase_total_carbon_emissions_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>

    <tr class="bg-zinc-50/70 border-y border-zinc-200/60">
      <td colspan="2" class="py-3 px-6 font-bold text-zinc-500 uppercase tracking-wider text-[10px]">
        03. Production Run-time Sub-Metrics
      </td>
    </tr>
    <tr class="hover:bg-zinc-50/40 transition-colors">
      <td class="py-3.5 px-6 pl-10 text-zinc-600 flex items-center gap-2.5">
        <span class="w-2 h-2 rounded-full bg-orange-500"></span>
        Usage Phase — per month
      </td>
      <td class="py-3.5 px-6 text-right font-mono text-zinc-900 font-medium text-base">
        {{ results?.usage_phase_carbon_emissions_per_month_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>
    <tr class="hover:bg-zinc-50/40 transition-colors">
      <td class="py-3.5 px-6 pl-10 text-zinc-600 flex items-center gap-2.5">
        <span class="w-2 h-2 rounded-full bg-orange-500"></span>
        Usage Phase — per user
      </td>
      <td class="py-3.5 px-6 text-right font-mono text-zinc-900 font-medium text-base">
        {{ results?.usage_phase_carbon_emissions_per_user_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>
    <tr class="bg-orange-50/40 font-semibold border-b border-zinc-200">
      <td class="py-3.5 px-6 pl-10 text-orange-900">
        Usage Phase — Total cumulative footprint
      </td>
      <td class="py-3.5 px-6 text-right font-mono text-orange-800 text-base">
        {{ results?.usage_phase_total_carbon_emissions_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>

    <tr class="bg-emerald-50/50 border-t-2 border-b-4 border-zinc-950/80 font-bold text-lg">
      <td class="py-5 px-6 text-emerald-950 font-formal-serif tracking-tight">
        TOTAL CARBON FOOTPRINT
      </td>
      <td class="py-5 px-6 text-right font-mono text-emerald-900 text-xl">
        {{ results?.total_carbon_emissions_kgCO2eq?.toFixed(6) ?? '—' }}
      </td>
    </tr>
  </tbody>
</table>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import {computed} from 'vue';

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

// --- High-Precision Percentages (Strict 5 Decimal Spaces) ---
const devPct = computed(() => {
  if (!props.results || !props.results.total_carbon_emissions_kgCO2eq) return '0.00000';
  return ((props.results.dev_phase_total_carbon_emissions_kgCO2eq / props.results.total_carbon_emissions_kgCO2eq) * 100).toFixed(5);
});

const deployPct = computed(() => {
  if (!props.results || !props.results.total_carbon_emissions_kgCO2eq) return '0.00000';
  return ((props.results.deploy_phase_total_carbon_emissions_kgCO2eq / props.results.total_carbon_emissions_kgCO2eq) * 100).toFixed(5);
});

const usagePct = computed(() => {
  if (!props.results || !props.results.total_carbon_emissions_kgCO2eq) return '0.00000';
  return ((props.results.usage_phase_total_carbon_emissions_kgCO2eq / props.results.total_carbon_emissions_kgCO2eq) * 100).toFixed(5);
});

// --- Mathematical SVG Gauge Calculations ---
const RADIUS = 42;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS; // ~263.89378

const devRatio = computed(() => parseFloat(devPct.value) / 100 || 0);
const deployRatio = computed(() => parseFloat(deployPct.value) / 100 || 0);
const usageRatio = computed(() => parseFloat(usagePct.value) / 100 || 0);

const devDasharray = computed(() => `${devRatio.value * CIRCUMFERENCE} ${CIRCUMFERENCE}`);
const deployDasharray = computed(() => `${deployRatio.value * CIRCUMFERENCE} ${CIRCUMFERENCE}`);
const usageDasharray = computed(() => `${usageRatio.value * CIRCUMFERENCE} ${CIRCUMFERENCE}`);

const deployOffset = computed(() => -(devRatio.value * CIRCUMFERENCE));
const usageOffset = computed(() => -((devRatio.value + deployRatio.value) * CIRCUMFERENCE));

const formatValue = (val: number | null | undefined) => {
  return val == null ? '—' : val.toFixed(4);
};
</script>