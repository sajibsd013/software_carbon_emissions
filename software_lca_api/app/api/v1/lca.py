from fastapi import APIRouter, HTTPException
from app.schemas.lca_schema import DevPhaseLCARequest, DevPhaseLCAResponse
from app.services.dev_phase_lca_service import DevPhaseLCACalculator

router = APIRouter()

@router.post("/calculate-lca", response_model=DevPhaseLCAResponse)
async def calculate_lca(request: DevPhaseLCARequest):
    try:
        project_dict = request.project_data.model_dump()
        calculator = DevPhaseLCACalculator(
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