export const useEmissionsCalculator = () => {
  const BASE_URL = 'http://localhost:8000';

  const currentMode = useState('currentMode', () => 'github');
  const githubData = useState('githubData', () => null);
  const autoFilledValues = useState('autoFilledValues', () => ({}));
  const showResults = useState('showResults', () => false);
  const loading = useState('loading', () => false);
  const results = useState('results', () => null);

  const switchMode = (mode: string) => {
    currentMode.value = mode;
  };

  const showToast = (msg: string, type = 'error') => {
    const event = new CustomEvent('show-toast', { detail: { msg, type } });
    window.dispatchEvent(event);
  };

  const fetchGitHubData = async (owner: string, repo: string, months: number) => {
    if (!owner || !repo) {
      showToast('Enter owner and repository name.');
      return false;
    }

    loading.value = true;
    try {
      const res = await fetch(`${BASE_URL}/api/v1/github-data`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ owner, repo, months })
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      githubData.value = data;
      autoFilledValues.value = {
        months: data.months || months,
        repo_size_gb: data.repo_size_gb,
        avg_monthly_active_contributors: data.avg_monthly_active_contributors,
        total_ci_runs: data.total_ci_runs,
        total_ci_duration_minutes: data.total_ci_duration_minutes,
        total_commits: data.total_commits
      };

      showToast('GitHub data fetched!', 'success');
      return true;
    } catch (e) {
      showToast('Fetch failed: ' + e.message);
      return false;
    } finally {
      loading.value = false;
    }
  };

  const calculateEmissions = async (payload: any) => {
    loading.value = true;
    try {
      const res = await fetch(`${BASE_URL}/api/v1/calculate-emissions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      if (data.status !== 'success') throw new Error('API error');

      results.value = data.results;
      showResults.value = true;
      showToast('Emissions calculated!', 'success');
      return true;
    } catch (e) {
      showToast('Calculation failed: ' + e.message);
      return false;
    } finally {
      loading.value = false;
    }
  };

  const buildPayload = (formData: any) => {
    const shared = {
      total_deployments: parseInt(formData.total_deployments),
      deployment_duration_minutes: parseFloat(formData.deployment_duration),
      cloud_region: formData.cloud_region,
      monthly_active_users: parseInt(formData.monthly_users),
      avg_monthly_usage_hours_per_use: parseFloat(formData.usage_hours),
      avg_monthly_data_transfer_gb: parseFloat(formData.data_transfer),
      db_migration_gb: parseFloat(formData.db_migration),
      docker_image_size_gb: parseFloat(formData.docker_size),
      dependency_size_gb: parseFloat(formData.dep_size),
      server_uptime_hours_per_month: parseFloat(formData.server_uptime),
      server_instance_power_w: parseFloat(formData.server_power),
      assumptions: formData.assumptions
    };

    if (currentMode.value === 'github') {
      return { ...autoFilledValues.value, ...shared };
    } else {
      return {
        months: parseInt(formData.months),
        repo_size_gb: parseFloat(formData.repo_size_gb),
        avg_monthly_active_contributors: parseInt(formData.contributors),
        total_ci_runs: parseInt(formData.ci_runs),
        total_ci_duration_minutes: parseFloat(formData.ci_duration),
        total_commits: parseInt(formData.commits),
        ...shared
      };
    }
  };

  return {
    currentMode,
    githubData,
    autoFilledValues,
    showResults,
    loading,
    results,
    switchMode,
    fetchGitHubData,
    calculateEmissions,
    buildPayload,
    showToast
  };
};

