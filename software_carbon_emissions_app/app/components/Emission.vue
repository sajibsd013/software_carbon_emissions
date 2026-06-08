<template>
  <!-- Explicit typography definitions injected locally for absolute rendering safety -->
  <component :is="'style'">
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    .font-formal-serif {
      font-family: 'Lora', Georgia, serif;
    }
    .font-formal-sans {
      font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    }
  </component>

  <section class="relative font-formal-sans text-gray-900 w-full">

    <!-- MODAL OVERLAY: GitHub Query Matrix -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-zinc-900/60 backdrop-blur-sm p-4">
        <div class="bg-white rounded-2xl shadow-xl border border-zinc-200 w-full max-w-lg p-6 sm:p-8 overflow-hidden transform transition-all">

          <!-- Header block inside dialog overlay -->
          <div class="flex justify-between items-center pb-4 mb-5 border-b border-zinc-100">
            <div>
              <h3 class="text-xs font-bold text-zinc-400 uppercase tracking-widest">Fetch from GitHub</h3>
              <p class="text-base font-semibold text-zinc-900 font-formal-serif mt-0.5">Automated Repository Scan</p>
            </div>
            <button @click="isModalOpen = false" class="text-zinc-400 hover:text-zinc-600 p-1.5 rounded-lg hover:bg-zinc-50 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <!-- Parameter inputs for API payload -->
          <div class="space-y-4 mb-6 text-sm">
            <div>
              <label class="block font-semibold text-zinc-700 mb-1.5">Owner</label>
              <input v-model="formData.owner" type="text" class="w-full px-3.5 py-2.5 bg-white border border-zinc-300 rounded-lg shadow-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 outline-none transition-all text-base placeholder-zinc-400" placeholder="e.g. axios" />
            </div>
            <div>
              <label class="block font-semibold text-zinc-700 mb-1.5">Repository</label>
              <input v-model="formData.repo" type="text" class="w-full px-3.5 py-2.5 bg-white border border-zinc-300 rounded-lg shadow-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 outline-none transition-all text-base placeholder-zinc-400" placeholder="e.g. axios" />
            </div>
            <div>
              <label class="block font-semibold text-zinc-700 mb-1.5">Analysis Period (months)</label>
              <input v-model.number="formData.months" type="number" class="w-full px-3.5 py-2.5 bg-white border border-zinc-300 rounded-lg shadow-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100 outline-none transition-all text-base" min="1" max="24" />
            </div>
          </div>

          <!-- Fire action -->
          <button @click="handleFetchGithub" :disabled="loading"
            class="w-full py-3 px-4 flex items-center justify-center gap-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl font-medium shadow-sm transition-colors disabled:opacity-50">
            <span v-if="loading" class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
            <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.929.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
            </svg>
            <span>Fetch from GitHub</span>
          </button>
        </div>
      </div>
    </Transition>

    <!-- MAIN CONFIGURATION CONTENT WORKSPACE -->
    <div class="space-y-6 sm:space-y-8">

      <!-- HEADER WORKSPACE TRIGGER CALLOUT -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 bg-white border border-zinc-200 shadow-sm rounded-xl">
        <div>
          <h3 class="text-xs font-semibold text-[#6b7c6b] uppercase tracking-wider mb-0">Basic Data
            <span class="ml-1 text-gray-400 normal-case">{{ repoLabel ? `for ${repoLabel}` : '' }}</span>
          </h3>
        </div>

        <button @click="isModalOpen = true"
          class="inline-flex items-center justify-center gap-2 px-4 py-2 text-sm font-semibold bg-zinc-900 text-white hover:bg-zinc-800 rounded-lg transition-colors shadow-sm self-start sm:self-center">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.929.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
          </svg>
          Fetch via GitHub
        </button>
      </div>

      <!-- FORM BLOCK 1: Development Environment Metric Groups -->
      <div class="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
        <div class="flex items-center gap-2 mb-4 pb-2 border-b border-zinc-100">
          <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
          <h3 class="text-xs font-bold text-zinc-500 uppercase tracking-widest font-formal-sans">Baseline Project Metrics</h3>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 text-sm">
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Months</label>
            <input v-model.number="formData.months" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Repo Size (GB)</label>
            <input v-model.number="formData.repo_size_gb" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" step="0.001" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Avg Monthly Contributors</label>
            <input v-model.number="formData.avg_monthly_active_contributors" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Total CI Runs</label>
            <input v-model.number="formData.total_ci_runs" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">CI Duration (min)</label>
            <input v-model.number="formData.total_ci_duration_minutes" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Total Commits</label>
            <input v-model.number="formData.total_commits" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
          </div>
        </div>
      </div>

      <!-- FORM BLOCK 2: Deployment & Cloud Production Metric Groups -->
      <div class="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
        <div class="flex items-center gap-2 mb-4 pb-2 border-b border-zinc-100">
          <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
          <h3 class="text-xs font-bold text-zinc-500 uppercase tracking-widest font-formal-sans">Emission Parameters</h3>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5 text-sm">
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Total Deployments</label>
            <input v-model.number="formData.total_deployments" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Deployment Duration (min)</label>
            <input v-model.number="formData.deployment_duration_minutes" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Cloud Region</label>
            <select v-model="formData.cloud_region" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base">
              <optgroup label="── AWS ──────────────────">
                <option value="us-east-1">us-east-1 — N. Virginia</option>
                <option value="us-west-2">us-west-2 — Oregon</option>
                <option value="eu-west-1">eu-west-1 — Ireland</option>
                <option value="eu-central-1">eu-central-1 — Frankfurt</option>
                <option value="ap-southeast-1">ap-southeast-1 — Singapore</option>
                <option value="ap-northeast-1">ap-northeast-1 — Tokyo</option>
                <option value="ap-south-1">ap-south-1 — Mumbai</option>
                <option value="sa-east-1">sa-east-1 — São Paulo</option>
                <option value="cn-north-1">cn-north-1 — Beijing</option>
              </optgroup>
              <optgroup label="── Azure ─────────────────">
                <option value="eastus">eastus — Virginia</option>
                <option value="westus2">westus2 — Washington</option>
                <option value="northeurope">northeurope — Ireland</option>
                <option value="westeurope">westeurope — Netherlands</option>
                <option value="southeastasia">southeastasia — Singapore</option>
                <option value="centralindia">centralindia — India</option>
                <option value="brazilsouth">brazilsouth — São Paulo</option>
                <option value="chinaeast2">chinaeast2 — China</option>
              </optgroup>
              <optgroup label="── GCP ───────────────────">
                <option value="us-central1">us-central1 — Iowa</option>
                <option value="us-east1">us-east1 — South Carolina</option>
                <option value="europe-west1">europe-west1 — Belgium</option>
                <option value="europe-west3">europe-west3 — Frankfurt</option>
                <option value="asia-southeast1">asia-southeast1 — Singapore</option>
                <option value="asia-south1">asia-south1 — Mumbai</option>
                <option value="asia-east2">asia-east2 — Hong Kong</option>
              </optgroup>
              <optgroup label="── DigitalOcean ──────────">
                <option value="nyc">nyc — New York</option>
                <option value="sfo3">sfo3 — San Francisco</option>
                <option value="lon1">lon1 — London</option>
                <option value="ams3">ams3 — Amsterdam</option>
                <option value="fra1">fra1 — Frankfurt</option>
                <option value="sgp1">sgp1 — Singapore</option>
                <option value="blr1">blr1 — Bangalore</option>
              </optgroup>
            </select>
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Monthly Active Users</label>
            <input v-model.number="formData.monthly_active_users" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Avg Usage hrs/User</label>
            <input v-model.number="formData.avg_monthly_usage_hours_per_user" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" step="0.5" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Monthly Data Transfer (GB)</label>
            <input v-model.number="formData.avg_monthly_data_transfer_gb" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" step="0.1" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Docker Image Size (GB)</label>
            <input v-model.number="formData.docker_image_size_gb" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" step="0.001" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">DB Migration (GB)</label>
            <input v-model.number="formData.db_migration_gb" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" step="0.001" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Dependency Size (GB)</label>
            <input v-model.number="formData.dependency_size_gb" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" step="0.001" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Server Uptime (hrs/month)</label>
            <input v-model.number="formData.server_uptime_hours_per_month" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
          </div>
          <div>
            <label class="block font-medium text-zinc-600 mb-1">Artifact Size (GB)</label>
            <input v-model.number="formData.avg_artifact_size_gb" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" step="0.00001" />
          </div>
        </div>
      </div>

      <!-- FORM BLOCK 3: Collapsible Structural Assumptions & Modifiers -->
      <div class="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
        <button @click="showAssumptions = !showAssumptions"
          class="w-full flex items-center justify-between font-bold text-xs uppercase tracking-widest text-zinc-500 outline-none group">
          <span class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-zinc-400 group-hover:bg-zinc-600 transition-colors"></span>
            Advanced Assumptions
          </span>
          <svg :class="['w-4 h-4 text-zinc-400 transform transition-transform duration-200', showAssumptions && 'rotate-90']" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>

        <Transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 translate-y-[-10px]"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 translate-y-[-10px]"
        >
          <div v-if="showAssumptions" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5 mt-5 pt-4 border-t border-zinc-100 text-sm">
            <div>
              <label class="block font-medium text-zinc-600 mb-1">Client Desktop User (%)</label>
              <input v-model.number="formData.assumptions.CLIENT_DESKTOP_PERCENT" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
            </div>
            <div>
              <label class="block font-medium text-zinc-600 mb-1">Client Laptop User (%)</label>
              <input v-model.number="formData.assumptions.CLIENT_LAPTOP_PERCENT" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
            </div>
            <div>
              <label class="block font-medium text-zinc-600 mb-1">Client Mobile User (%)</label>
              <input v-model.number="formData.assumptions.CLIENT_MOBILE_OR_TAB_PERCENT" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
            </div>
            <div>
              <label class="block font-medium text-zinc-600 mb-1">Developer Desktop User (%)</label>
              <input v-model.number="formData.assumptions.DEVELOPER_DESKTOP_PERCENT" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
            </div>
            <div>
              <label class="block font-medium text-zinc-600 mb-1">Developer Laptop User (%)</label>
              <input v-model.number="formData.assumptions.DEVELOPER_LAPTOP_PERCENT" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
            </div>
            <div>
              <label class="block font-medium text-zinc-600 mb-1">Developer Work (hrs/month)</label>
              <input v-model.number="formData.assumptions.DEVELOPER_WORK_HOURS_PER_MONTH" type="number" class="w-full px-3 py-2 bg-zinc-50/50 border border-zinc-200 rounded-lg outline-none focus:bg-white focus:border-zinc-400 transition-colors text-base" />
            </div>
          </div>
        </Transition>
      </div>

      <!-- OPERATIONAL EXECUTION TRIGGER BUTTON -->
      <div class="flex flex-col items-center justify-center pt-4">
        <button @click="handleCalculateEmissions" :disabled="loading"
          class="px-8 py-4 flex items-center justify-center gap-2 bg-emerald-700 hover:bg-emerald-800 disabled:opacity-60 text-white font-medium text-base rounded-xl shadow-md shadow-emerald-900/10 hover:shadow-lg transition-all min-w-[240px]">
          <span v-if="loading" class="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></span>
          <svg v-else width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
          <span>Calculate Emissions</span>
        </button>
      </div>

      <!-- RESULTS REPORTING PANEL OUTPUT MOUNT HOOK -->
      <ResultsPanel :results="results" :repo-label="repoLabel" />
    </div>

    <!-- Telemetry Messaging Ports -->
    <Toast ref="toastRef" />
    <GithubLoader :isLoading="gitLoading" />
  </section>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

const showAssumptions = ref(true);
const isModalOpen = ref(false);
const loading = ref(false);
const gitLoading = ref(false);
const repoLabel = ref('');

const formData = reactive({
  owner: '',
  repo: '',
  months: 12,
  repo_size_gb: 0.85,
  avg_monthly_active_contributors: 14,
  total_ci_runs: 1450,
  total_ci_duration_minutes: 17400,
  total_commits: 1250,
  total_deployments: 180,
  deployment_duration_minutes: 1440,
  cloud_region: 'us-east-1',
  monthly_active_users: 45000,
  avg_monthly_usage_hours_per_user: 18.5,
  avg_monthly_data_transfer_gb: 1250.5,
  db_migration_gb: 4.5,
  docker_image_size_gb: 1.15,
  dependency_size_gb: 0.65,
  server_uptime_hours_per_month: 730,
  avg_artifact_size_gb: 0.12,
  assumptions: {
    CLIENT_DESKTOP_PERCENT: 35,
    CLIENT_LAPTOP_PERCENT: 45,
    CLIENT_MOBILE_OR_TAB_PERCENT: 20,
    DEVELOPER_DESKTOP_PERCENT: 15,
    DEVELOPER_LAPTOP_PERCENT: 85,
    DEVELOPER_WORK_HOURS_PER_MONTH: 160
  }
});

const BASE_URL = 'http://127.0.0.1:8000/v1';
const toastRef = ref<any>(null);

const showToast = (msg: string, type = 'error') => {
  toastRef.value?.show(msg, type);
};

const handleFetchGithub = async () => {
  const { owner, repo, months } = formData;
  if (!owner || !repo) {
    showToast('Enter owner and repository name.');
    return;
  }

  gitLoading.value = true;
  loading.value = true;

  try {
    const res = await fetch(`${BASE_URL}/github-data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ owner, repo, months })
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const responseData = await res.json();
    if (responseData.status !== 'success') throw new Error('API response failed.');

    formData.repo_size_gb = responseData.repo_size_gb;
    formData.avg_monthly_active_contributors = responseData.avg_monthly_active_contributors;
    formData.total_ci_runs = responseData.total_ci_runs;
    formData.total_ci_duration_minutes = responseData.total_ci_duration_minutes;
    formData.total_commits = responseData.total_commits;
    formData.avg_artifact_size_gb = responseData.avg_artifact_size_gb;

    repoLabel.value = `${owner}/${repo}`;
    showToast('GitHub metrics successfully synchronized.', 'success');
  } catch (e: any) {
    showToast('Synchronization failed: ' + e.message);
  } finally {
    gitLoading.value = false;
    loading.value = false;
    isModalOpen.value = false;
  }
};

const results = ref(null);

const handleCalculateEmissions = async () => {
  loading.value = true;
  try {
    const payload = {
      ...formData,
      assumptions: {
        CLIENT_DESKTOP_PERCENT: formData.assumptions.CLIENT_DESKTOP_PERCENT / 100,
        CLIENT_LAPTOP_PERCENT: formData.assumptions.CLIENT_LAPTOP_PERCENT / 100,
        CLIENT_MOBILE_OR_TAB_PERCENT: formData.assumptions.CLIENT_MOBILE_OR_TAB_PERCENT / 100,
        DEVELOPER_DESKTOP_PERCENT: formData.assumptions.DEVELOPER_DESKTOP_PERCENT / 100,
        DEVELOPER_LAPTOP_PERCENT: formData.assumptions.DEVELOPER_LAPTOP_PERCENT / 100,
        DEVELOPER_WORK_HOURS_PER_MONTH: formData.assumptions.DEVELOPER_WORK_HOURS_PER_MONTH
      }
    };

    const res = await fetch(`${BASE_URL}/calculate-emissions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (data.status !== 'success') throw new Error('API execution failed.');

    results.value = data.results;
    showToast('Emissions successfully appended to ledger.', 'success');
  } catch (e: any) {
    showToast('Analysis processing failed: ' + e.message);
  } finally {
    loading.value = false;
  }
};
</script>