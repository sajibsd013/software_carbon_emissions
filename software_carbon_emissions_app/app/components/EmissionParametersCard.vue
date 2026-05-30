<template>
  <div class="panel p-4.5">
    <div class="text-xs font-semibold text-[#6b7c6b] uppercase tracking-wider mb-3">Emission Parameters</div>

    <div class="grid grid-cols-3 gap-2.5">
      <div>
        <label class="field-label">Total Deployments</label>
        <input v-model.number="params.total_deployments" type="number" class="input-field" />
      </div>
      <div>
        <label class="field-label">Deployment Duration (min)</label>
        <input v-model.number="params.deployment_duration" type="number" class="input-field" />
      </div>

      <div class="">
        <label class="field-label">Cloud Region</label>
        <select v-model="params.cloud_region" class="input-field">
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
        <input v-model.number="params.monthly_users" type="number" class="input-field" />
      </div>
      <div>
        <label class="field-label">Avg Usage hrs/User</label>
        <input v-model.number="params.usage_hours" type="number" class="input-field" step="0.5" />
      </div>
      <div>
        <label class="field-label">Monthly Data Transfer (GB)</label>
        <input v-model.number="params.data_transfer" type="number" class="input-field" step="0.1" />
      </div>
      <div>
        <label class="field-label">Docker Image Size (GB)</label>
        <input v-model.number="params.docker_size" type="number" class="input-field" step="0.001" />
      </div>
      <div>
        <label class="field-label">DB Migration (GB)</label>
        <input v-model.number="params.db_migration" type="number" class="input-field" step="0.001" />
      </div>
      <div>
        <label class="field-label">Dependency Size (GB)</label>
        <input v-model.number="params.dep_size" type="number" class="input-field" step="0.001" />
      </div>
      <div>
        <label class="field-label">Server Uptime (hrs/month)</label>
        <input v-model.number="params.server_uptime" type="number" class="input-field" />
      </div>
      <div>
        <label class="field-label">Artifact Size (GB)</label>
        <input v-model.number="params.artifact_size" type="number" class="input-field" step="0.00001" />
      </div>
    </div>

    <hr class="divider">

    <!-- Assumptions Toggle -->
    <button @click="showAssumptions = !showAssumptions"
      class="bg-none border-none cursor-pointer flex items-center gap-1.5 text-xs font-medium text-[#6b7c6b] p-0">
      <svg :class="['w-3 h-3 chevron', showAssumptions && 'open']" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2.5">
        <path d="M9 18l6-6-6-6" />
      </svg>
      Advanced Assumptions
    </button>

    <div v-if="showAssumptions" class="grid grid-cols-3 gap-2.5 mt-3">

      <div>
        <label class="field-label">Client Desktop User (%)</label>
        <input v-model.number="assumptions.desktop_pct" type="number" class="input-field" step="1" />
      </div>
      <div>
        <label class="field-label">Client Laptop User (%)</label>
        <input v-model.number="assumptions.laptop_pct" type="number" class="input-field" step="1" />
      </div>
      <div>
        <label class="field-label">Client Mobile User (%)</label>
        <input v-model.number="assumptions.mobile_pct" type="number" class="input-field" step="1" />
      </div>

      <div>
        <label class="field-label">Developer Desktop User (%)</label>
        <input v-model.number="assumptions.dev_desktop_pct" type="number" class="input-field" step="1" />
      </div>
      <div>
        <label class="field-label">Developer Laptop User (%)</label>
        <input v-model.number="assumptions.dev_laptop_pct" type="number" class="input-field" step="1" />
      </div>
      <div>
        <label class="field-label">Developer Work (hrs/month)</label>
        <input v-model.number="assumptions.work_hours" type="number" class="input-field" />
      </div>
    </div>

    <hr class="divider">

    <button @click="emit('calculate')" :disabled="loading"
      class="btn-primary w-full py-2.5 flex items-center justify-center gap-1.75">
      <span v-if="loading" class="spinner"></span>
      <span v-if="!loading">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
        </svg>

      </span>
      Calculate Emissions
    </button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['calculate']);

const showAssumptions = ref(true);

const params = ref({
  total_deployments: 0,
  deployment_duration: 0,
  cloud_region: 'us-east-1',
  monthly_users: 0,
  usage_hours: 0,
  data_transfer: 0,
  docker_size: 0,
  db_migration: 0,
  dep_size: 0,
  server_uptime: 720,
  artifact_size: 0,

});

const assumptions = ref({
  desktop_pct: 25,
  laptop_pct: 45,
  mobile_pct: 30,
  dev_desktop_pct: 25,
  dev_laptop_pct: 75,
  work_hours: 10
});

defineExpose({
  getParams: () => params.value,
  getAssumptions: () => assumptions.value
});
</script>
