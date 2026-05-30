<template>
  <div v-if="!showResults" class="panel min-h-96 flex flex-col items-center justify-center text-center border-dashed border-[#d1dbd1]">
    <div class="w-13 h-13 bg-[#f0fdf4] border border-[#bbf7d0] rounded-2xl flex items-center justify-center mb-3.5">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="1.5">
        <path d="M3 3v18h18"/>
        <path d="M18 9l-5 5-4-4-3 3"/>
      </svg>
    </div>
    <div class="text-base font-semibold text-[#374151] mb-1">No results yet</div>
    <div class="text-sm text-[#9ca89c] max-w-60 leading-relaxed">Fetch GitHub data or fill in values manually, then calculate emissions.</div>
  </div>

  <div v-else class="result-section visible flex flex-col gap-4">
    <!-- Summary -->
    <div class="panel p-4.5">
      <div class="flex items-center justify-between mb-3.5">
        <div class="text-sm font-semibold text-[#1a2e1a]">Emission Summary</div>
        <span class="text-xs font-medium bg-[#f0fdf4] border border-[#bbf7d0] text-[#15803d] px-2 py-0.75 rounded-full">
          {{ repoLabel }}
        </span>
      </div>

      <div class="grid grid-cols-[1.4fr_1fr_1fr_1fr] gap-2.5 mb-4">
        <div class="metric-card">
          <div class="metric-value">{{ results?.total_carbon_emissions_kgCO2eq?.toFixed(2) ?? '—' }}</div>
          <div class="metric-label">Total kgCO₂eq</div>
        </div>
        <div class="metric-card">
          <div class="metric-value" style="color: #d97706">{{ results?.dev_phase_total_carbon_emissions_kgCO2eq?.toFixed(2) ?? '—' }}</div>
          <div class="metric-label">Development</div>
        </div>
        <div class="metric-card">
          <div class="metric-value" style="color: #2563eb">{{ results?.deploy_phase_total_carbon_emissions_kgCO2eq?.toFixed(4) ?? '—' }}</div>
          <div class="metric-label">Deployment</div>
        </div>
        <div class="metric-card">
          <div class="metric-value" style="color: #ea580c">{{ results?.usage_phase_total_carbon_emissions_kgCO2eq?.toFixed(2) ?? '—' }}</div>
          <div class="metric-label">Usage</div>
        </div>
      </div>

      <div class="flex flex-col gap-2">
        <div>
          <div class="flex justify-between text-xs text-[#6b7c6b] mb-1">
            <span>Development</span>
            <span class="font-medium">{{ devPct }}%</span>
          </div>
          <div class="bar-track">
            <div class="phase-bar" style="background: #d97706" :style="{ width: devPct + '%' }"></div>
          </div>
        </div>
        <div>
          <div class="flex justify-between text-xs text-[#6b7c6b] mb-1">
            <span>Deployment</span>
            <span class="font-medium">{{ deployPct }}%</span>
          </div>
          <div class="bar-track">
            <div class="phase-bar" style="background: #2563eb" :style="{ width: deployPct + '%' }"></div>
          </div>
        </div>
        <div>
          <div class="flex justify-between text-xs text-[#6b7c6b] mb-1">
            <span>Usage</span>
            <span class="font-medium">{{ usagePct }}%</span>
          </div>
          <div class="bar-track">
            <div class="phase-bar" style="background: #ea580c" :style="{ width: usagePct + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chart + Per-unit -->
    <div class="grid grid-cols-2 gap-4">
      <div class="panel p-4.5">
        <div class="text-sm font-semibold text-[#1a2e1a] mb-3">Phase Distribution</div>
        <div class="relative h-48">
          <canvas ref="chartCanvas"></canvas>
        </div>
      </div>
      <div class="panel p-4.5">
        <div class="text-sm font-semibold text-[#1a2e1a] mb-3">Per-Unit Metrics</div>
        <div class="flex flex-col gap-0">
          <div class="flex justify-between py-2 border-b border-[#e8eee8]">
            <span class="text-xs text-[#6b7c6b]">Per Commit</span>
            <span class="text-xs font-semibold text-[#1a2e1a]">{{ formatValue(results?.dev_phase_carbon_emissions_per_commit_kgCO2eq) }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[#e8eee8]">
            <span class="text-xs text-[#6b7c6b]">Per CI Run</span>
            <span class="text-xs font-semibold text-[#1a2e1a]">{{ formatValue(results?.dev_phase_carbon_emissions_per_ci_kgCO2eq) }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[#e8eee8]">
            <span class="text-xs text-[#6b7c6b]">Per Release</span>
            <span class="text-xs font-semibold text-[#1a2e1a]">{{ formatValue(results?.deploy_phase_carbon_emissions_per_release_kgCO2eq) }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-[#e8eee8]">
            <span class="text-xs text-[#6b7c6b]">Per User</span>
            <span class="text-xs font-semibold text-[#1a2e1a]">{{ formatValue(results?.usage_phase_carbon_emissions_per_user_kgCO2eq) }}</span>
          </div>
          <div class="flex justify-between py-2">
            <span class="text-xs text-[#6b7c6b]">Dev / Month</span>
            <span class="text-xs font-semibold text-[#1a2e1a]">{{ formatValue(results?.dev_phase_carbon_emissions_per_month_kgCO2eq) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Full Breakdown -->
    <div class="panel p-4.5">
      <div class="text-sm font-semibold text-[#1a2e1a] mb-3">Full Breakdown</div>
      <table class="w-full border-collapse">
        <thead>
          <tr class="text-xs font-semibold text-[#9ca89c] uppercase tracking-wider">
            <th class="text-left p-1.5 pb-1.5">Metric</th>
            <th class="text-right p-1.5 pb-1.5">kgCO₂eq</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in breakdownRows" :key="row.label" class="breakdown-row">
            <td :style="{ color: row.bold ? '#1a2e1a' : '#4b5563' }" :class="row.bold ? 'font-semibold' : 'font-normal'" class="py-2 text-xs">
              <span :style="{ background: row.color }" class="inline-block w-2 h-2 rounded-sm mr-1.75 align-middle"></span>
              {{ row.label }}
            </td>
            <td :style="{ color: row.color }" :class="row.bold ? 'font-bold' : 'font-medium'" class="text-right py-2 text-xs">
              {{ row.val?.toFixed(6) ?? '—' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

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

const chartCanvas = ref(null);
let chartInstance = null;

const showResults = computed(() => !!props.results);

const devPct = computed(() => {
  if (!props.results) return '0';
  const total = props.results.total_carbon_emissions_kgCO2eq;
  return ((props.results.dev_phase_total_carbon_emissions_kgCO2eq / total) * 100).toFixed(1);
});

const deployPct = computed(() => {
  if (!props.results) return '0';
  const total = props.results.total_carbon_emissions_kgCO2eq;
  return ((props.results.deploy_phase_total_carbon_emissions_kgCO2eq / total) * 100).toFixed(1);
});

const usagePct = computed(() => {
  if (!props.results) return '0';
  const total = props.results.total_carbon_emissions_kgCO2eq;
  return ((props.results.usage_phase_total_carbon_emissions_kgCO2eq / total) * 100).toFixed(1);
});

const breakdownRows = computed(() => {
  if (!props.results) return [];
  return [
    { label: 'Dev — per month', val: props.results.dev_phase_carbon_emissions_per_month_kgCO2eq, color: '#d97706' },
    { label: 'Dev — per commit', val: props.results.dev_phase_carbon_emissions_per_commit_kgCO2eq, color: '#d97706' },
    { label: 'Dev — per CI run', val: props.results.dev_phase_carbon_emissions_per_ci_kgCO2eq, color: '#d97706' },
    { label: 'Dev — total', val: props.results.dev_phase_total_carbon_emissions_kgCO2eq, color: '#d97706' },
    { label: 'Deploy — per release', val: props.results.deploy_phase_carbon_emissions_per_release_kgCO2eq, color: '#2563eb' },
    { label: 'Deploy — total', val: props.results.deploy_phase_total_carbon_emissions_kgCO2eq, color: '#2563eb' },
    { label: 'Usage — per month', val: props.results.usage_phase_carbon_emissions_per_month_kgCO2eq, color: '#ea580c' },
    { label: 'Usage — per user', val: props.results.usage_phase_carbon_emissions_per_user_kgCO2eq, color: '#ea580c' },
    { label: 'Usage — total', val: props.results.usage_phase_total_carbon_emissions_kgCO2eq, color: '#ea580c' },
    { label: 'TOTAL', val: props.results.total_carbon_emissions_kgCO2eq, color: '#15803d', bold: true }
  ];
});

const formatValue = (val) => {
  return val == null ? '—' : val.toFixed(4) + ' kg';
};

const renderChart = () => {
  if (!chartCanvas.value || !props.results) return;

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new ChartJS(chartCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['Development', 'Deployment', 'Usage'],
      datasets: [{
        data: [
          props.results.dev_phase_total_carbon_emissions_kgCO2eq,
          props.results.deploy_phase_total_carbon_emissions_kgCO2eq,
          props.results.usage_phase_total_carbon_emissions_kgCO2eq
        ],
        backgroundColor: ['rgba(217,119,6,0.15)', 'rgba(37,99,235,0.15)', 'rgba(234,88,12,0.15)'],
        borderColor: ['#d97706', '#2563eb', '#ea580c'],
        borderWidth: 2,
        hoverOffset: 5
      }]
    },
    options: {
      cutout: '70%',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#6b7c6b',
            font: { family: 'Inter', size: 11, weight: '500' },
            padding: 14,
            boxWidth: 10,
            boxHeight: 10,
            usePointStyle: true,
            pointStyle: 'rectRounded'
          }
        },
        tooltip: {
          callbacks: { label: c => ` ${c.parsed.toFixed(4)} kgCO₂eq` },
          backgroundColor: '#fff',
          borderColor: '#e2e8e2',
          borderWidth: 1,
          titleColor: '#1a2e1a',
          bodyColor: '#6b7c6b'
        }
      }
    }
  });
};

watch(() => props.results, () => {
  nextTick(() => {
    renderChart();
  });
}, { deep: true });

onMounted(() => {
  if (props.results) {
    renderChart();
  }
});

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>
