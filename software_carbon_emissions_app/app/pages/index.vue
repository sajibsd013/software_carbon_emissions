<template>
  <div class="min-h-screen bg-[#f5f7f5]">
    <AppHeader />

    <main class="max-w-6xl mx-auto px-6 py-7">
      <!-- Page heading -->
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-[#1a2e1a] mb-1">Software Carbon Footprint Analyzer</h2>
        <p class="text-sm text-[#6b7c6b]">Measure development, deployment, and usage phase emissions from GitHub or manual data.</p>
      </div>

      <Emission/>
      
      <!-- <div class="flex flex-col gap-4">
        <div class="flex flex-col gap-4">
          <DataSourceCard
            ref="dataSourceRef"
            :mode="currentMode"
            :loading="loading"
            @mode-change="handleModeChange"
            @fetch-github="handleFetchGithub"
          />

          <EmissionParametersCard
            ref="emissionParamsRef"
            :loading="loading"
            @calculate="handleCalculate"
          />
        </div>

        <ResultsPanel
          :results="results"
          :repo-label="repoLabel"
        />
      </div> -->
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





const currentMode = ref('github');
const githubData = ref(null);
const autoFilledValues = ref({});
const results = ref(null);
const loading = ref(false);
const repoLabel = ref('Manual Entry');

const dataSourceRef = ref(null);
const emissionParamsRef = ref(null);
const toastRef = ref(null);

const handleModeChange = (mode) => {
  currentMode.value = mode;
};

const showToast = (msg, type = 'error') => {
  toastRef.value?.show(msg, type);
};

const handleFetchGithub = async (data) => {
  const { owner, repo, months } = data;

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

    githubData.value = responseData;
    autoFilledValues.value = {
      months: responseData.months || months,
      repo_size_gb: responseData.repo_size_gb,
      avg_monthly_active_contributors: responseData.avg_monthly_active_contributors,
      total_ci_runs: responseData.total_ci_runs,
      total_ci_duration_minutes: responseData.total_ci_duration_minutes,
      total_commits: responseData.total_commits,
      avg_artifact_size_gb: responseData.avg_artifact_size_gb
    };

    // Update preview
    const previewData = {
      'Repo Size': (responseData.repo_size_gb ?? 0).toFixed(4) + ' GB',
      'Total Commits': (responseData.total_commits ?? 0).toLocaleString(),
      'CI Runs': (responseData.total_ci_runs ?? 0).toLocaleString(),
      'CI Duration': (responseData.total_ci_duration_minutes ?? 0).toFixed(0) + ' min',
      'Contributors': responseData.total_contributors ?? '—',
      'Avg/Month': responseData.avg_monthly_active_contributors ?? '—',
      'Avg/Artifact': (responseData.avg_artifact_size_gb ?? 0).toFixed(4) + ' GB'
    };

    dataSourceRef.value?.setPreviewData(previewData);

    // Update repo label
    repoLabel.value = `${owner}/${repo}`;

    showToast('GitHub data fetched!', 'success');
  } catch (e) {
    showToast('Fetch failed: ' + e.message);
  } finally {
    loading.value = false;
  }
};

const handleCalculate = async () => {
  if (currentMode.value === 'github' && !githubData.value) {
    showToast('Please fetch GitHub data first.');
    return;
  }

  loading.value = true;

  try {
    const dataSourceData = currentMode.value === 'github' ? {} : dataSourceRef.value?.getManualData() || {};
    const paramData = emissionParamsRef.value?.getParams() || {};
    const assumptionsData = emissionParamsRef.value?.getAssumptions() || {};

    const payload = buildPayload(dataSourceData, paramData, assumptionsData);

    const res = await fetch(`${BASE_URL}/api/v1/calculate-emissions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    if (data.status !== 'success') throw new Error('API error');

    results.value = data.results;
    showToast('Emissions calculated!', 'success');
  } catch (e) {
    showToast('Calculation failed: ' + e.message);
  } finally {
    loading.value = false;
  }
};

const buildPayload = (dataSourceData, paramData, assumptionsData) => {
  const shared = {
    total_deployments: paramData.total_deployments,
    deployment_duration_minutes: paramData.deployment_duration,
    cloud_region: paramData.cloud_region,
    monthly_active_users: paramData.monthly_users,
    avg_monthly_usage_hours_per_use: paramData.usage_hours,
    avg_monthly_data_transfer_gb: paramData.data_transfer,
    db_migration_gb: paramData.db_migration,
    docker_image_size_gb: paramData.docker_size,
    dependency_size_gb: paramData.dep_size,
    server_uptime_hours_per_month: paramData.server_uptime,
    avg_artifact_size_gb: paramData.artifact_size,
    assumptions: {
      CLIENT_DESKTOP_PERCENT: assumptionsData.desktop_pct/100,
      CLIENT_LAPTOP_PERCENT: assumptionsData.laptop_pct/100,
      CLIENT_MOBILE_OR_TAB_PERCENT: assumptionsData.mobile_pct/100,
      DEVELOPER_DESKTOP_PERCENT: assumptionsData.dev_desktop_pct/100,
      DEVELOPER_LAPTOP_PERCENT: assumptionsData.dev_laptop_pct/100,
      DEVELOPER_WORK_HOURS_PER_MONTH: assumptionsData.work_hours
    }
  };

  if (currentMode.value === 'github') {
    return { ...autoFilledValues.value, ...shared };
  } else {
    return {
      months: dataSourceData.months,
      repo_size_gb: dataSourceData.repo_size_gb,
      avg_monthly_active_contributors: dataSourceData.contributors,
      total_ci_runs: dataSourceData.ci_runs,
      total_ci_duration_minutes: dataSourceData.ci_duration,
      total_commits: dataSourceData.commits,
      ...shared
    };
  }
};
</script>

