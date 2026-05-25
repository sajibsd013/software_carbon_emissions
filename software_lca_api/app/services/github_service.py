import httpx
import asyncio
import datetime
from dateutil import parser

class GitHubDataFetcher:
    BASE_URL = "https://api.github.com/repos"

    def __init__(self, repo_name: str, token: str = None, days: int = 30):
        self.repo_name = repo_name
        self.headers = {"Authorization": f"token {token}"} if token else {}
        self.since_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
        self.project_data = {
            'repo_name': self.repo_name,
            'repo_size_mb': 0.0,
            'monthly_commits': 0,
            'active_contributors': 0,
            'ci_runs_per_month': 0,
            'ci_avg_duration_min': 0.0
        }

    async def fetch_repo_stats(self, client: httpx.AsyncClient):
        response = await client.get(f"{self.BASE_URL}/{self.repo_name}")
        print(f"Repo stats response status: {response.status_code}")
        if response.status_code == 200:
            self.project_data['repo_size_mb'] = response.json().get("size", 0) / 1024.0
        else:
            raise Exception(f"Failed to fetch repository stats: {response.text}")
    async def fetch_commit_data(self, client: httpx.AsyncClient):
        all_commits = []
        page = 1
        active_emails = set()
        while True:
            url = f"{self.BASE_URL}/{self.repo_name}/commits?since={self.since_date.isoformat()}&per_page=100&page={page}"
            response = await client.get(url)
            print(f"Commit data response status: {response.status_code}")
            if response.status_code != 200 or not response.json():
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
            print(f"CI data response status: {response.status_code}")
            if response.status_code != 200 or not response.json().get("workflow_runs"):
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
        async with httpx.AsyncClient(headers=self.headers, timeout=15.0) as client:
            await asyncio.gather(
                self.fetch_repo_stats(client),
                self.fetch_commit_data(client),
                self.fetch_ci_data(client)
            )
        return self.project_data