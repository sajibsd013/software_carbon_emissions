from pydantic import BaseModel, Field
from typing import Optional, Dict

"""
        Expected kwargs:

        Development Phase (mandatory):
            - months (int/float)
            - repo_size_gb (float)
            - avg_monthly_active_contributors (int)
            - total_ci_runs (int)
            - total_ci_duration_minutes (float)
            - total_commits (int)

        Deployment Phase (mandatory):
            - total_deployments (int)
            - deployment_duration_minutes (float)
            - cloud_region (str)

        Usage Phase (mandatory):
            - monthly_active_users (int/float)  
            - avg_monthly_usage_hours_per_user (float)
            - avg_monthly_data_transfer_gb (float) — avg GB transferred per user per month (up + down)

        Optional:
            - db_migration_gb (float)                  — default 0.0
            - docker_image_size_gb (float)             — default 0.0
            - dependency_size_gb (float)               — default 0.0
            - server_uptime_hours_per_month (float)    — default 0.0
            - server_instance_power_w (float)          — default 0.0
            - assumptions (dict)                       — override any constant
"""

class SoftwareCarbonEmissionRequest(BaseModel):
    # Development Phase
    months: int = Field(12, ge=1, le=36, description="Timeframe to analyze")
    repo_size_gb: float = Field(0.025753, ge=0, description="Size of the repository in GB")
    avg_monthly_active_contributors: int = Field(16, ge=0, description="Average monthly active contributors")
    total_ci_runs: int = Field(8634, ge=0, description="Total number of CI runs")
    total_ci_duration_minutes: float = Field(12771.733333 	, ge=0, description="Total duration of CI runs in minutes")
    total_commits: int = Field(8634, ge=0, description="Total number of commits")

    # Deployment Phase
    total_deployments: int = Field(12, ge=0, description="Total number of deployments")
    deployment_duration_minutes: float = Field(60, ge=0, description="Average duration of each deployment in minutes")
    cloud_region: str = Field("us-east-1", description="Cloud region for deployment")

    # Usage Phase
    monthly_active_users: int = Field(1000, ge=0, description="Number of monthly active users")
    avg_monthly_usage_hours_per_user: float = Field(2.0, ge=0, description="Average monthly usage hours per user")
    avg_monthly_data_transfer_gb: float = Field(5.0, ge=0, description="Average monthly data transfer per user in GB")

    # Optional parameters with defaults
    db_migration_gb: float = Field(0.0, ge=0, description="Data migrated during database migration in GB")
    docker_image_size_gb: float = Field(0.065, ge=0, description="Size of the Docker image in GB")
    dependency_size_gb: float = Field(0.005, ge=0, description="Size of dependencies in GB")
    server_uptime_hours_per_month: float = Field(0.0, ge=0, description="Server uptime in hours per month")
    server_instance_power_w: float = Field(0.0, ge=0, description="Average power consumption of server instances in watts")

    assumptions: Optional[Dict[str, float]] = Field(
        None, 
        example={
            'DEVELOPER_LAPTOP_PERCENT': 0.75,
            'DEVELOPER_DESKTOP_PERCENT': 0.25,
            'DEVELOPER_LAPTOP_AVG_POWER_W': 45,
            'DEVELOPER_DESKTOP_AVG_POWER_W': 250,
            'ARTIFACT_SIZE': 0.000580,
            'DEVELOPER_WORK_HOURS_PER_MONTH': 10,
            'CLIENT_LAPTOP_PERCENT': 0.45,
            'CLIENT_DESKTOP_PERCENT': 0.25,
            'CLIENT_MOBILE_OR_TAB_PERCENT': 0.30,
            'CLIENT_LAPTOP_AVG_POWER_W': 45,
            'CLIENT_DESKTOP_AVG_POWER_W': 250,
            'CLIENT_MOBILE_OR_TAB_AVG_POWER_W': 5,
        }
    )

class SoftwareCarbonEmissionResponse(BaseModel):
    status: str
    results: Dict[str, float] 