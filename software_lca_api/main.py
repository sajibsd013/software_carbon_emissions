from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict
import uvicorn
import os
from dotenv import load_dotenv

from lca_calculator import GitHubDataFetcher, LCACalculator

load_dotenv()

app = FastAPI(
    title="DevPhase LCA API",
    description="Separated microservices for GitHub data collection and Carbon LCA calculation."
)

# --- PYDANTIC MODELS ---

class GitHubDataRequest(BaseModel):
    repo_name: str = Field(..., example="django/django")
    days: int = Field(30, ge=1, le=365, description="Timeframe to analyze")

class ProjectMetrics(BaseModel):
    repo_name: str
    repo_size_mb: float
    monthly_commits: int
    active_contributors: int
    ci_runs_per_month: int
    ci_avg_duration_min: float

class LCARequest(BaseModel):
    project_data: ProjectMetrics
    custom_assumptions: Optional[Dict[str, float]] = Field(
        None, 
        example={
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
    )

# --- API ENDPOINTS ---

@app.post("/api/v1/github-data", response_model=ProjectMetrics)
async def get_github_data(request: GitHubDataRequest):
    """
    API 1: Collects raw data from GitHub.
    """
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        print(f"Using GitHub Token: {'Yes' if github_token else 'No'}")
        
        fetcher = GitHubDataFetcher(
            repo_name=request.repo_name,
            token=github_token,
            days=request.days
        )
        
        project_data = await fetcher.get_all_data()
        return project_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch GitHub data: {str(e)}")


@app.post("/api/v1/calculate-lca")
async def calculate_lca(request: LCARequest):
    """
    API 2: Calculates Carbon Footprint based on provided project data.
    """
    try:
        # We convert the Pydantic model to a standard dictionary to pass to our calculator
        project_dict = request.project_data.dict()
        
        calculator = LCACalculator(
            project_data=project_dict,
            custom_assumptions=request.custom_assumptions
        )
        
        emissions = calculator.calculate_emissions()
        
        return {
            "status": "success",
            "repository": project_dict["repo_name"],
            "results": emissions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate LCA: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)