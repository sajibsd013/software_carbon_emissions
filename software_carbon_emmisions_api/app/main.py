from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import github
from app.api.v1 import software_carbon_emmisions

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Separated microservices for GitHub data collection and Carbon Emissions calculation."
)

# Include the routers from our modular files
app.include_router(github.router, prefix="/api/v1", tags=["GitHub"])
app.include_router(software_carbon_emmisions.router, prefix="/api/v1", tags=["Carbon Emissions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Software Carbon Emissions API. Visit /docs for the swagger UI."}