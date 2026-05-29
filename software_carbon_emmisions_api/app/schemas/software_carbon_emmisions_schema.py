from pydantic import BaseModel, Field
from typing import Optional, Dict

class SoftwareCarbonEmissionRequest(BaseModel):
    months: int = Field(12, ge=1, le=36, description="Timeframe to analyze")
    repo_size_gb: float = Field(0.025753, ge=0, description="Size of the repository in GB")
    avg_monthly_active_contributors: int = Field(16, ge=0, description="Average monthly active contributors")
    total_ci_runs: int = Field(8634, ge=0, description="Total number of CI runs")
    total_ci_duration_minutes: float = Field(12771.733333 	, ge=0, description="Total duration of CI runs in minutes")
    docker_image_size_gb: float = Field(0.065, ge=0, description="Size of the Docker image in GB")
    dependency_size_gb: float = Field(0.005, ge=0, description="Size of dependencies in GB")
    assumptions: Optional[Dict[str, float]] = Field(
        None, 
        example={
            'LAPTOP_PERCENT': 0.75,
            'DESKTOP_PERCENT': 0.25,
            'DEVELOPER_LAPTOP_AVG_POWER_W': 45,
            'DEVELOPER_DESKTOP_AVG_POWER_W': 250,
            'ARTIFACT_SIZE': 0.000580,
            'DEVELOPER_WORK_HOURS_PER_MONTH': 10,
        }
    )

class SoftwareCarbonEmissionResponse(BaseModel):
    status: str
    results: Dict[str, float] 