from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import github, lca

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Separated microservices for GitHub data collection and Carbon LCA calculation."
)

# Include the routers from our modular files
app.include_router(github.router, prefix="/api/v1", tags=["GitHub"])
app.include_router(lca.router, prefix="/api/v1", tags=["LCA"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Software LCA API. Visit /docs for the swagger UI."}