from fastapi import APIRouter, HTTPException
from app.schemas.github_schema import GitHubDataRequest, ProjectMetrics
from app.services.github_service import GitHubDataFetcher
from app.core.config import settings

router = APIRouter()

@router.post("/github-data", response_model=ProjectMetrics)
async def get_github_data(request: GitHubDataRequest):
    try:
        print(f"Received request for repo: {request.repo} with months: {request.months}")  
        fetcher = GitHubDataFetcher(
            repo = request.repo,
            owner=request.owner,
            api_token=settings.GITHUB_TOKEN,
            months=request.months
        )
        project_data = await fetcher.get_project_data()
        return {
            "status": "success",
            **project_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch GitHub data: {str(e)}")