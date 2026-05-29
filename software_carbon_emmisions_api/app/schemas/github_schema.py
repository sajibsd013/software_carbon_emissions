from pydantic import BaseModel, Field

class GitHubDataRequest(BaseModel):
    owner: str = Field(..., example="axios")
    repo: str = Field(..., example="axios")
    months: int = Field(12, ge=1, le=36, description="Timeframe to analyze")

class ProjectMetrics(BaseModel):
    status: str
    owner: str 
    repo: str 
    repo_size_gb: float 
    total_commits: int 
    avg_monthly_active_contributors: int 
    total_contributors: int 
    total_ci_runs: int
    total_ci_duration_minutes: float
    avg_artifact_size_gb: float