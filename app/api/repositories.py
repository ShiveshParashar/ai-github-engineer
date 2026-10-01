from fastapi import (
    APIRouter,
    HTTPException
)

from pydantic import (
    BaseModel,
    HttpUrl
)

from app.services.git_service import (
    clone_repository
)

from app.agents.orchestrator import (
    run_repository_analysis
)


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"]
)


class RepositoryRequest(BaseModel):

    url: HttpUrl


@router.post("/analyze")
def analyze_repository(
    request: RepositoryRequest
):

    try:

        repository_url = str(
            request.url
        )

        # Clone repository
        repository_path = clone_repository(
            repository_url
        )

        # Run complete analysis
        analysis = run_repository_analysis(
            repository_path=repository_path,
            repository_url=repository_url
        )

        return {
            "repository_url": repository_url,
            "analysis": analysis
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )