<template>
  <div class="panel p-4.5">
    <div class="text-xs font-semibold text-[#6b7c6b] uppercase tracking-wider mb-2.5">Base Data</div>

    <!-- Tab switcher -->
    <div class="grid grid-cols-2 gap-1 bg-[#f5f7f5] border border-[#e2e8e2] rounded-lg p-1 mb-4">
      <button @click="emit('mode-change', 'github')" :class="['tab-pill', mode === 'github' && 'active']">
        GitHub Fetch
      </button>
      <button @click="emit('mode-change', 'manual')" :class="['tab-pill', mode === 'manual' && 'active']">
        Manual Entry
      </button>
    </div>

    <!-- GitHub Mode -->
    <div v-if="mode === 'github'">
      <div class="grid grid-cols-3 gap-2.5 mb-6">
        <div>
          <label class="field-label">Owner</label>
          <input v-model="github.owner" type="text" class="input-field" placeholder="e.g. axios" />
        </div>
        <div>
          <label class="field-label">Repository</label>
          <input v-model="github.repo" type="text" class="input-field" placeholder="e.g. axios" />
        </div>
        <div>
          <label class="field-label">Analysis Period (months)</label>
          <input v-model.number="github.months" type="number" class="input-field" min="1" max="24" />
        </div>
      </div>

      <button @click="handleFetchGithub" :disabled="loading"
        class="btn-primary w-full py-2 flex items-center justify-center gap-1.75 ">
        <span v-if="loading" class="spinner"></span>
        <span v-if="!loading">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.929.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
          </svg>
        </span>
          <span>Fetch from GitHub</span>

      </button>

      <div v-if="showPreview" class="gh-preview">
        <div class="text-xs font-semibold text-[#15803d] uppercase tracking-wider mb-2">✓ Data fetched — auto-filled
          below</div>
        <div class="grid grid-cols-2 gap-2">
          <div v-for="(value, label) in previewData" :key="label">
            <div class="text-xs font-medium text-[#6b9b6b] uppercase tracking-wider">{{ label }}</div>
            <div class="text-sm font-semibold text-[#15803d] mt-0.5">{{ value }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Manual Mode -->
    <div v-else>
      <div class="grid grid-cols-3 gap-2.5">
        <div>
          <label class="field-label">Months</label>
          <input v-model.number="manual.months" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">Repo Size (GB)</label>
          <input v-model.number="manual.repo_size_gb" type="number" class="input-field" step="0.001" />
        </div>
        <div>
          <label class="field-label">Avg Monthly Contributors</label>
          <input v-model.number="manual.contributors" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">Total CI Runs</label>
          <input v-model.number="manual.ci_runs" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">CI Duration (min)</label>
          <input v-model.number="manual.ci_duration" type="number" class="input-field" />
        </div>
        <div>
          <label class="field-label">Total Commits</label>
          <input v-model.number="manual.commits" type="number" class="input-field" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  mode: {
    type: String,
    default: 'github'
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['mode-change', 'fetch-github', 'update-data']);

const github = ref({
  owner: '',
  repo: '',
  months: 12
});

const manual = ref({
  months: 12,
  repo_size_gb: null,
  contributors: null,
  ci_runs: null,
  ci_duration: null,
  commits: null,
  avg_artifact_size_gb: null,
});

const showPreview = ref(false);
const previewData = ref({});

const handleFetchGithub = () => {
  emit('fetch-github', github.value);
};

watch(() => props.mode, (newMode) => {
  if (newMode === 'github') {
    showPreview.value = false;
  }
});

defineExpose({
  setPreviewData: (data) => {
    previewData.value = data;
    showPreview.value = true;
  },
  getGithubData: () => github.value,
  getManualData: () => manual.value
});
</script>
