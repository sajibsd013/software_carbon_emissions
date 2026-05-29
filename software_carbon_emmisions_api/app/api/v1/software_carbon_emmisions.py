from fastapi import APIRouter, HTTPException
from app.schemas.software_carbon_emmisions_schema import SoftwareCarbonEmissionRequest, SoftwareCarbonEmissionResponse
from app.services.software_carbon_emmisions_service import SoftwareCarbonEmission

router = APIRouter()

@router.post("/calculate-emissions", response_model=SoftwareCarbonEmissionResponse)
async def calculate_emissions(request: SoftwareCarbonEmissionRequest):
    try:
        project_dict = request.model_dump()
        calculator = SoftwareCarbonEmission(
            *project_dict.values(),
        )
        emissions = calculator.calculate_emissions()
        
        return {
            "status": "success",
            "results": emissions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate Carbon Emissions: {str(e)}")