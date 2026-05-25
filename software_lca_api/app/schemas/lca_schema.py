from pydantic import BaseModel, Field
from typing import Optional, Dict
from app.schemas.github_schema import ProjectMetrics

class DevPhaseLCARequest(BaseModel):
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

class DevPhaseLCAResponse(BaseModel):
    status: str
    repository: str
    results: Dict[str, float] 