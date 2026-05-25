from pydantic import BaseModel, Field

class GitHubDataRequest(BaseModel):
    repo_name: str = Field(..., example="django/django")
    days: int = Field(30, ge=1, le=365, description="Timeframe to analyze")

class ProjectMetrics(BaseModel):
    status: str
    repo_name: str = Field(..., example="django/django")
    repo_size_mb: float = Field(..., example=273.2900390625)
    monthly_commits: int = Field(..., example=106)
    active_contributors: int = Field(..., example=33)
    ci_runs_per_month: int = Field(..., example=9375)
    ci_avg_duration_min: float = Field(..., example= 0.878275555555541)