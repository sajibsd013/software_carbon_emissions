from fastapi import APIRouter, HTTPException
from app.schemas.github_schema import GitHubDataRequest, ProjectMetrics
from app.services.github_service import GitHubDataFetcher
from app.core.config import settings

router = APIRouter()

@router.post("/github-data", response_model=ProjectMetrics)
async def get_github_data(request: GitHubDataRequest):
    try:
        print(f"Received request for repo: {request.repo_name} with days: {request.days}")  
        print(f"settings.GITHUB_TOKEN: {settings.GITHUB_TOKEN}")  # Debugging: Check if the token is loaded correctly
        fetcher = GitHubDataFetcher(
            repo_name=request.repo_name,
            token=settings.GITHUB_TOKEN,
            days=request.days
        )
        project_data = await fetcher.get_all_data()
        return {
            "status": "success",
            **project_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch GitHub data: {str(e)}")