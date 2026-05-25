import httpx
import asyncio
import datetime
from dateutil import parser

class GitHubDataFetcher:
    """Handles all asynchronous communication with the GitHub API."""
    BASE_URL = "https://api.github.com/repos"

    def __init__(self, repo_name: str, token: str = None, days: int = 30):
        self.repo_name = repo_name
        self.headers = {"Authorization": f"token {token}", } if token else {}
        self.since_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
        self.project_data = {
            'repo_name': self.repo_name,
            'repo_size_mb': 0,
            'monthly_commits': 0,
            'active_contributors': 0,
            'ci_runs_per_month': 0,
            'ci_avg_duration_min': 0
        }

    async def fetch_repo_stats(self, client: httpx.AsyncClient):
        response = await client.get(f"{self.BASE_URL}/{self.repo_name}")
        print(f"Fetching repo stats for {self.repo_name} - Status: {response.status_code}")
        if response.status_code == 200:
            self.project_data['repo_size_mb'] = response.json().get("size", 0) / 1024.0

    async def fetch_commit_data(self, client: httpx.AsyncClient):
        all_commits = []
        page = 1
        active_emails = set()

        while True:
            url = f"{self.BASE_URL}/{self.repo_name}/commits?since={self.since_date.isoformat()}&per_page=100&page={page}"
            response = await client.get(url)
            print(f"Fetching commit data for {self.repo_name} - Status: {response.status_code}")
            if response.status_code != 200 or not response.json():
                print(f"Error fetching commit data for {self.repo_name} - Status: {response.status_code}")
                break
            data = response.json()
            all_commits.extend(data)
            
            for commit in data:
                try:
                    active_emails.add(commit['commit']['author']['email'])
                except (KeyError, TypeError):
                    continue
            page += 1

        self.project_data['monthly_commits'] = len(all_commits)
        self.project_data['active_contributors'] = len(active_emails)

    async def fetch_ci_data(self, client: httpx.AsyncClient):
        total_runs = 0
        total_duration_minutes = 0.0
        page = 1

        while True:
            url = f"{self.BASE_URL}/{self.repo_name}/actions/runs?per_page=100&page={page}"
            response = await client.get(url)
            print(f"Fetching CI data for {self.repo_name} - Status: {response.status_code}")
            if response.status_code != 200 or not response.json().get("workflow_runs"):
                print(f"Error fetching CI data for {self.repo_name} - Status: {response.status_code}")
                break
                
            runs = response.json()["workflow_runs"]
            out_of_date_range = False
            
            for run in runs:
                created_at = parser.isoparse(run["created_at"])
                if created_at < self.since_date:
                    out_of_date_range = True
                    break
                    
                if run["status"] == "completed" and run.get("updated_at"):
                    updated_at = parser.isoparse(run["updated_at"])
                    duration = (updated_at - created_at).total_seconds() / 60.0
                    total_duration_minutes += duration
                    total_runs += 1
                    
            if out_of_date_range:
                break
            page += 1

        self.project_data['ci_runs_per_month'] = total_runs
        self.project_data['ci_avg_duration_min'] = total_duration_minutes / total_runs if total_runs > 0 else 0

    async def get_all_data(self):
        """Fires all GitHub requests concurrently and returns the dataset."""
        async with httpx.AsyncClient(headers=self.headers, timeout=15.0) as client:
            await asyncio.gather(
                self.fetch_repo_stats(client),
                self.fetch_commit_data(client),
                self.fetch_ci_data(client)
            )
        return self.project_data


class LCACalculator:
    """Handles the mathematical Life Cycle Assessment based on provided data."""
    def __init__(self, project_data: dict, custom_assumptions: dict = None):
        self.project_data = project_data
        
        # Default Assumptions
        self.assumptions = {
            'DEVELOPER_WORK_HOURS_PER_MONTH': 10,
            'DEVICE_POWER': 45,
            'DEVELOPER_MACHINES_GRID_INTENSITY': 436,
            'DEVICE_EMBODIED_CARBON': 320_000,
            'DEVICE_LIFETIME_HOURS': 35_040,
            'CI_GRID_INTENSITY': 380,
            'CI_PUE': 1.2,
            'CI_CPU_POWER': 7.68,
            'CI_EMBODIED_CARBON': 1_200_000,
            'CI_SERVER_LIFETIME_HOURS': 35_040,
            'CI_CORE_SHARE': 2,
            'CI_TOTAL_CORES': 96,
            'DATA_TRANSFER_GRID_INTENSITY': 380,
            'ELECTRICITY_PER_GB': 0.001
        }
        if custom_assumptions:
            self.assumptions.update(custom_assumptions)

    def calculate_emissions(self):
        a = self.assumptions
        p = self.project_data
        
        # 1. Developer Machines
        dev_hours = p.get('active_contributors', 0) * a['DEVELOPER_WORK_HOURS_PER_MONTH']
        dev_e = (a['DEVICE_POWER'] * dev_hours) / 1000.0
        dev_m = (a['DEVICE_EMBODIED_CARBON'] / a['DEVICE_LIFETIME_HOURS']) * dev_hours 
        dev_total = (dev_e * a['DEVELOPER_MACHINES_GRID_INTENSITY']) + dev_m

        # 2. CI/CD
        ci_hours = (p.get('ci_runs_per_month', 0) * p.get('ci_avg_duration_min', 0)) / 60.0 
        ci_e = ci_hours * a['CI_CPU_POWER'] * a['CI_PUE'] / 1000.0
        ci_m = (a['CI_EMBODIED_CARBON'] / a['CI_SERVER_LIFETIME_HOURS']) * (a['CI_CORE_SHARE'] / a['CI_TOTAL_CORES']) * ci_hours 
        ci_total = (ci_e * a['CI_GRID_INTENSITY']) + ci_m

        # 3. Data Transfer
        gb = (p.get('repo_size_mb', 0) * p.get('ci_runs_per_month', 0)) / 1024.0
        data_total = (gb * a['ELECTRICITY_PER_GB']) * a['DATA_TRANSFER_GRID_INTENSITY']

        # Totals
        total = dev_total + ci_total + data_total
        commits = p.get('monthly_commits', 1) or 1 

        return {
            "dev_machines_gCO2eq": {
                "value": round(dev_total, 2),
                "unit": "gCO2eq",
                "title": "Developer Machines Carbon Footprint",
            },
            "ci_cd_gCO2eq": {
                "value": round(ci_total, 2),
                "unit": "gCO2eq",
                "title": "CI/CD Carbon Footprint",
            },
            "data_transfer_gCO2eq": {
                "value": round(data_total, 2),
                "unit": "gCO2eq",
                "title": "Data Transfer Carbon Footprint",
            },
            "total_monthly_gCO2eq": {
                "value": round(total, 2),
                "unit": "gCO2eq",
                "title": "Total Monthly Carbon Footprint",
            },
            "per_commit_gCO2eq": {
                "value": round(total / commits, 2),
                "unit": "gCO2eq",
                "title": "Carbon Footprint per Commit",
            }
        }