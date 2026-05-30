<template>
  <section class="relative">

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md p-5 border border-[#e2e8e2]">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-sm font-semibold text-[#6b7c6b] uppercase tracking-wider">Fetch from GitHub</h3>
          <button @click="isModalOpen = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="space-y-4 mb-6">
          <div>
            <label class="field-label block mb-1">Owner</label>
            <input v-model="formData.owner" type="text" class="input-field w-full" placeholder="e.g. axios" />
          </div>
          <div>
            <label class="field-label block mb-1">Repository</label>
            <input v-model="formData.repo" type="text" class="input-field w-full" placeholder="e.g. axios" />
          </div>
          <div>
            <label class="field-label block mb-1">Analysis Period (months)</label>
            <input v-model.number="formData.months" type="number" class="input-field w-full" min="1" max="24" />
          </div>
        </div>

        <button @click="handleFetchGithub" :disabled="loading"
          class="btn-primary w-full py-2.5 flex items-center justify-center gap-2 bg-[#15803d] text-white rounded hover:bg-[#166534] disabled:opacity-50 transition-colors">
          <span v-if="loading"
            class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
          <span v-if="!loading">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.929.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
            </svg>
          </span>
          <span>Fetch from GitHub</span>
        </button>
      </div>
    </div>

    <div class="panel p-4.5">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xs font-semibold text-[#6b7c6b] uppercase tracking-wider mb-0">Basic Data</h3>

        <button @click="isModalOpen = true"
          class="text-xs font-medium bg-[#f5f7f5] border border-[#e2e8e2] px-3 py-1.5 rounded hover:bg-[#e2e8e2] transition-colors flex items-center gap-1.5">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.929.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
          </svg>
          Fetch via GitHub
        </button>
      </div>

      <div class="grid grid-cols-3 gap-2.5">
        <div>
          <label class="field-label">Months</label>
          <input v-model.number="formData.months" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">Repo Size (GB)</label>
          <input v-model.number="formData.repo_size_gb" type="number" class="input-field" step="0.001" />
        </div>
        <div>
          <label class="field-label">Avg Monthly Contributors</label>
          <input v-model.number="formData.avg_monthly_active_contributors" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">Total CI Runs</label>
          <input v-model.number="formData.total_ci_runs" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">CI Duration (min)</label>
          <input v-model.number="formData.total_ci_duration_minutes" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">Total Commits</label>
          <input v-model.number="formData.total_commits" type="number" class="input-field" />
        </div>
      </div>
      <hr class="divider">

      <h3 class="text-xs font-semibold text-[#6b7c6b] uppercase tracking-wider mt-5 mb-2.5">Emission Parameters</h3>

      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
        <div>
          <label class="field-label">Total Deployments</label>
          <input v-model.number="formData.total_deployments" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">Deployment Duration (min)</label>
          <input v-model.number="formData.deployment_duration_minutes" type="number" class="input-field" />
        </div>

        <div class="">
          <label class="field-label">Cloud Region</label>
          <select v-model="formData.cloud_region" class="input-field">
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
          <label class="field-label">Monthly Active Users</label>
          <input v-model.number="formData.monthly_active_users" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">Avg Usage hrs/User</label>
          <input v-model.number="formData.avg_monthly_usage_hours_per_user" type="number" class="input-field"
            step="0.5" />
        </div>
        <div>
          <label class="field-label">Monthly Data Transfer (GB)</label>
          <input v-model.number="formData.avg_monthly_data_transfer_gb" type="number" class="input-field" step="0.1" />
        </div>
        <div>
          <label class="field-label">Docker Image Size (GB)</label>
          <input v-model.number="formData.docker_image_size_gb" type="number" class="input-field" step="0.001" />
        </div>
        <div>
          <label class="field-label">DB Migration (GB)</label>
          <input v-model.number="formData.db_migration_gb" type="number" class="input-field" step="0.001" />
        </div>
        <div>
          <label class="field-label">Dependency Size (GB)</label>
          <input v-model.number="formData.dependency_size_gb" type="number" class="input-field" step="0.001" />
        </div>
        <div>
          <label class="field-label">Server Uptime (hrs/month)</label>
          <input v-model.number="formData.server_uptime_hours_per_month" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">Artifact Size (GB)</label>
          <input v-model.number="formData.avg_artifact_size_gb" type="number" class="input-field" step="0.00001" />
        </div>
      </div>

      <hr class="divider">

      <!-- Assumptions Toggle -->
      <button @click="showAssumptions = !showAssumptions"
        class="bg-none border-none cursor-pointer flex items-center gap-1.5 text-xs font-medium text-[#6b7c6b] p-0">
        <svg :class="['w-3 h-3 chevron', showAssumptions && 'open']" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2.5">
          <path d="M9 18l6-6-6-6" />
        </svg>
        Advanced Assumptions
      </button>

      <div v-if="showAssumptions" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5 mt-3">

        <div>
          <label class="field-label">Client Desktop User (%)</label>
          <input v-model.number="formData.assumptions.CLIENT_DESKTOP_PERCENT" type="number" class="input-field"
            step="1" />
        </div>
        <div>
          <label class="field-label">Client Laptop User (%)</label>
          <input v-model.number="formData.assumptions.CLIENT_LAPTOP_PERCENT" type="number" class="input-field"
            step="1" />
        </div>
        <div>
          <label class="field-label">Client Mobile User (%)</label>
          <input v-model.number="formData.assumptions.CLIENT_MOBILE_OR_TAB_PERCENT" type="number" class="input-field"
            step="1" />
        </div>

        <div>
          <label class="field-label">Developer Desktop User (%)</label>
          <input v-model.number="formData.assumptions.DEVELOPER_DESKTOP_PERCENT" type="number" class="input-field"
            step="1" />
        </div>
        <div>
          <label class="field-label">Developer Laptop User (%)</label>
          <input v-model.number="formData.assumptions.DEVELOPER_LAPTOP_PERCENT" type="number" class="input-field"
            step="1" />
        </div>
        <div>
          <label class="field-label">Developer Work (hrs/month)</label>
          <input v-model.number="formData.assumptions.DEVELOPER_WORK_HOURS_PER_MONTH" type="number"
            class="input-field" />
        </div>
      </div>

      <hr class="divider">
    </div>
    <Toast ref="toastRef" />
    <GithubLoader :isLoading="loading" />

  </section>

</template>


<script setup lang="ts">
import { ref, reactive } from 'vue';

const showAssumptions = ref(true);
const isModalOpen = ref(false);
const loading = ref(false);

const formData = reactive({
  owner: '',
  repo: '',
  months: 12,
  repo_size_gb: '',
  avg_monthly_active_contributors: '',
  total_ci_runs: '',
  total_ci_duration_minutes: '',
  total_commits: '',
  total_deployments: '',
  deployment_duration_minutes: '',
  cloud_region: '',
  monthly_active_users: '',
  avg_monthly_usage_hours_per_user: '',
  avg_monthly_data_transfer_gb: '',
  db_migration_gb: '',
  docker_image_size_gb: '',
  dependency_size_gb: '',
  server_uptime_hours_per_month: '',
  avg_artifact_size_gb: 12,
  assumptions: {
    CLIENT_DESKTOP_PERCENT: 25,
    CLIENT_LAPTOP_PERCENT: 30,
    CLIENT_MOBILE_OR_TAB_PERCENT: 45,
    DEVELOPER_DESKTOP_PERCENT: 25,
    DEVELOPER_LAPTOP_PERCENT: 75,
    DEVELOPER_WORK_HOURS_PER_MONTH: 160
  }
});

const BASE_URL = 'http://localhost:8000';

const toastRef = ref(null);

const showToast = (msg, type = 'error') => {
  toastRef.value?.show(msg, type);
};


const handleFetchGithub = async () => {
  const { owner, repo, months } = formData;

  if (!owner || !repo) {
    showToast('Enter owner and repository name.');
    return;
  }

  loading.value = true;

  try {
    const res = await fetch(`${BASE_URL}/api/v1/github-data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ owner, repo, months })
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const responseData = await res.json();
    if (responseData.status !== 'success') throw new Error('API error');
    formData.repo_size_gb = responseData.repo_size_gb;
    formData.avg_monthly_active_contributors = responseData.avg_monthly_active_contributors;
    formData.total_ci_runs = responseData.total_ci_runs;
    formData.total_ci_duration_minutes = responseData.total_ci_duration_minutes;
    formData.total_commits = responseData.total_commits;
    formData.avg_artifact_size_gb = responseData.avg_artifact_size_gb;

    isModalOpen.value = false;
    loading.value = false;
    showToast('GitHub data fetched!', 'success');
  } catch (e) {
    showToast('Fetch failed: ' + e.message);
  } finally {
    loading.value = false;
    isModalOpen.value = false;

  }
};
</script>