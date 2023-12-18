from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.dependencies.auth import get_user_from_request_state
from src.endpoint_services.watch_progress import WatchProgressUgcHandler, get_watch_progress_ugc_service
from src.models.movie_progress import MovieProgress
from src.models.user import User

router = APIRouter()


@router.post(
    '/',
    summary="User's watching progress",
    description="Accepts checkpoints of user's watching progress.",
)
async def handle_user_view_progress(
    movie: MovieProgress,
    user: User = Depends(get_user_from_request_state),
    progress_ugc_service: WatchProgressUgcHandler = Depends(get_watch_progress_ugc_service),
) -> JSONResponse:
    try:
        await progress_ugc_service.update(movie_progress=movie, user=user)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={'detail': "User's watch progress has been saved"},
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')
