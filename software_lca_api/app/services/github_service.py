import httpx
import asyncio
import datetime
from dateutil import parser
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser
from collections import defaultdict
import time
from math import ceil, isnan

from collections import defaultdict
from math import ceil
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser

import asyncio
import httpx
import time


class GitHubDataFetcher:

    def __init__(self, owner, repo, months=12, api_token=None):

        self.__current_date = datetime.now(timezone.utc)
        self.__repo_url = f"https://api.github.com/repos/{owner}/{repo}"

        self.__headers = {"Authorization": f"token {api_token}"} if api_token else {}

        self.project_data = {
            "repo": repo,
            "owner": owner,
            "months": months,
            "since_date": (self.__current_date - relativedelta(months=months)if months else None),
            "repo_size_gb": None,
            "total_commits": None,
            "avg_monthly_active_contributors": None,
            "total_contributors": None,
            "total_ci_runs": None,
            "total_ci_duration_minutes": None,
            "avg_artifact_size_gb": None,
        }

    async def __make_request(
        self,
        client: httpx.AsyncClient,
        url,
        params=None
    ):

        while True:

            response = await client.get(
                url,
                headers=self.__headers,
                params=params
            )

            if response.status_code in [403, 429]:
                remaining = response.headers.get("X-RateLimit-Remaining")

                if remaining and int(remaining) == 0:

                    reset_time = int(response.headers["X-RateLimit-Reset"])
                    sleep_time = (max(0,reset_time - int(time.time())) + 5)

                    print(f"Rate limit exceeded. "f"Sleeping {sleep_time}s")
                    await asyncio.sleep(sleep_time)
                    continue
            return response

    async def __get_repo_size(self,client: httpx.AsyncClient):

        response = await self.__make_request(client,self.__repo_url)

        if response.status_code != 200:
            print(f"Failed repo fetch: "f"{response.status_code}")
            return

        repo_data = response.json()
        repo_size_kb = repo_data.get("size", 0)

        self.project_data["repo_size_gb"] = (repo_size_kb / (1024 ** 2))

        created_at = parser.isoparse(
            repo_data["created_at"]
        )

        if self.project_data["months"] is None:

            self.project_data["since_date"] = created_at

            rd = relativedelta(
                self.__current_date,
                created_at
            )

            self.project_data["months"] = (
                rd.years * 12 + rd.months
            )

    async def __get_branches(self,client: httpx.AsyncClient):

        response = await self.__make_request(client,f"{self.__repo_url}/branches")

        if response.status_code != 200:
            return []

        data = response.json()
        return [b["name"] for b in data]

    async def __get_commits(self,client: httpx.AsyncClient,branches):

        all_commits = []
        seen_shas = set()
        for branch in branches:
            page = 1
            while True:

                params = {
                    "since": self.project_data[
                        "since_date"
                    ].strftime("%Y-%m-%dT%H:%M:%SZ"),

                    "sha": branch,
                    "per_page": 100,
                    "page": page,
                }

                response = await self.__make_request(
                    client,
                    f"{self.__repo_url}/commits",
                    params=params
                )

                if response.status_code != 200:
                    break

                data = response.json()

                if not data:
                    break

                for commit in data:
                    try:
                        sha = commit["sha"]
                        date_str = commit["commit"]["author"]["date"]

                        commit_date = parser.isoparse(date_str)

                        if (commit_date >=self.project_data["since_date"]and sha not in seen_shas):
                            seen_shas.add(sha)
                            all_commits.append(commit)

                    except Exception:
                        continue

                page += 1

        self.project_data["total_commits"] = len(seen_shas)

        return all_commits

    async def __get_contributors(self,all_commits):

        month_windows = defaultdict(set)
        total_contributors = set()
        for m in range(1,self.project_data["months"] + 1):
            month_windows[f"m{m}"] = set()

        for commit in all_commits:
            try:
                email = commit["commit"]["author"]["email"]
                total_contributors.add(email)
                commit_date = parser.isoparse(commit["commit"]["author"]["date"])

                for m in range(1,self.project_data["months"] + 1):

                    month_start = (self.__current_date -relativedelta(months=m))
                    month_end = (self.__current_date -relativedelta(months=m - 1))

                    if (month_start <= commit_date <month_end):
                        month_windows[f"m{m}"].add(email)

            except Exception:
                continue

        result = {k: len(v)for k, v in month_windows.items()}

        self.project_data[
            "total_contributors"
        ] = len(total_contributors)

        self.project_data["avg_monthly_active_contributors"] = ceil(sum(result.values()) / len(result))

    async def __get_ci_cd_data(self,client: httpx.AsyncClient):

        total_ci_runs = 0
        total_duration_minutes = 0.0
        start_date = self.project_data["since_date"]

        end_date = self.__current_date
        chunk_days = 3
        current_start = start_date

        while current_start < end_date:

            current_end = min(current_start +timedelta(days=chunk_days),end_date
            )
            page = 1
            while True:

                params = {
                    "created": (
                        f"{current_start.strftime('%Y-%m-%dT%H:%M:%SZ')}.."
                        f"{current_end.strftime('%Y-%m-%dT%H:%M:%SZ')}"
                    ),
                    "per_page": 100,
                    "page": page,
                }

                response = await self.__make_request(
                    client,
                    f"{self.__repo_url}/actions/runs",
                    params=params
                )

                if response.status_code != 200:
                    break

                data = response.json()

                workflow_runs = data.get(
                    "workflow_runs",
                    []
                )

                if not workflow_runs:
                    break

                for run in workflow_runs:

                    try:

                        if run.get("status") != "completed":
                            continue

                        started_at = parser.isoparse(
                            run.get("run_started_at")
                            or run["created_at"]
                        )

                        updated_at = parser.isoparse(
                            run["updated_at"]
                        )

                        duration = (
                            updated_at - started_at
                        )

                        total_duration_minutes += max(
                            0,
                            duration.total_seconds() / 60
                        )

                        total_ci_runs += 1

                    except Exception:
                        continue

                page += 1

            current_start = (current_end + timedelta(seconds=1))

        self.project_data["total_ci_runs"] = total_ci_runs

        self.project_data["total_ci_duration_minutes"] = total_duration_minutes

    async def __get_dynamic_artifact_size(
        self,
        client: httpx.AsyncClient
    ):

        page = 1
        total_size_bytes = 0
        total_artifacts = 0

        while True:

            response = await self.__make_request(
                client,
                f"{self.__repo_url}/actions/artifacts",
                params={
                    "per_page": 100,
                    "page": page
                }
            )

            if response.status_code != 200:
                break

            data = response.json()

            artifacts = data.get("artifacts",[])

            if not artifacts:
                break

            for artifact in artifacts:

                total_size_bytes += artifact.get("size_in_bytes",0)
                total_artifacts += 1

            page += 1

        self.project_data[
            "avg_artifact_size_gb"
        ] = (
            (
                total_size_bytes /
                total_artifacts
            ) / (1024 ** 3)
            if total_artifacts > 0
            else 0.0
        )

    async def get_project_data(self):

        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            await self.__get_repo_size(client)
            branches = await self.__get_branches(client)
            all_commits = await self.__get_commits(client,branches)
            await self.__get_contributors(all_commits)
            await asyncio.gather(
                self.__get_ci_cd_data(client),
                self.__get_dynamic_artifact_size(client),
            )

        return self.project_data