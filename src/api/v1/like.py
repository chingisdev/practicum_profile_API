from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auxiliary_services.ugc_handler import LikeUgcHandler
from src.core.decorators import catch_broker_exceptions
from src.dependencies.auth import get_user_from_request_state
from src.endpoint_services.like import get_movie_like_ugc_service, get_review_like_ugc_service
from src.models.user import User

router = APIRouter()


@router.post(
    '/movie/{movie_id}',
    summary="User's like for movie",
    description="Accepts of user's likes.",
)
@catch_broker_exceptions
async def like_movie(
    movie_id: str,
    user: User = Depends(get_user_from_request_state),
    like_ugc_handler: LikeUgcHandler = Depends(get_movie_like_ugc_service),
) -> JSONResponse:
    await like_ugc_handler.add_ugc_content(target_id=movie_id, user_id=user.id)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'CREATED'})


@router.delete(
    '/movie/{movie_id}',
    summary="User's dislike for movie",
    description="Accepts of user's dislike.",
)
@catch_broker_exceptions
async def dislike_movie(
    movie_id: str,
    user: User = Depends(get_user_from_request_state),
    like_ugc_handler: LikeUgcHandler = Depends(get_movie_like_ugc_service),
) -> JSONResponse:
    await like_ugc_handler.delete_ugc_content(target_id=movie_id, user_id=user.id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': 'DELETED'})


@router.post(
    '/review/{review_id}',
    summary="User's like for review",
    description="Accepts of user's likes.",
)
@catch_broker_exceptions
async def like_review(
    review_id: str,
    user: User = Depends(get_user_from_request_state),
    like_ugc_handler: LikeUgcHandler = Depends(get_review_like_ugc_service),
) -> JSONResponse:
    await like_ugc_handler.add_ugc_content(target_id=review_id, user_id=user.id)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'CREATED'})


@router.delete(
    '/review/{review_id}',
    summary="Remove user's like or unlike from review rating",
)
@catch_broker_exceptions
async def unlike_review(
    review_id: str,
    user: User = Depends(get_user_from_request_state),
    like_ugc_handler: LikeUgcHandler = Depends(get_review_like_ugc_service),
) -> JSONResponse:
    await like_ugc_handler.delete_ugc_content(target_id=review_id, user_id=user.id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': 'DELETED'})


@router.get(
    '/movie/{movie_id}',
    summary='Users likes for movies',
    description='Likes values for movie.',
)
@catch_broker_exceptions
async def get_movie_likes(
    movie_id: str,
    like_ugc_handler: LikeUgcHandler = Depends(get_movie_like_ugc_service),
) -> JSONResponse:
    likes = await like_ugc_handler.find_ugc_content(target_id=movie_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=likes)


@router.get(
    '/review/{review_id}',
    summary='Users like for reviews',
    description='Like values for a review.',
)
@catch_broker_exceptions
async def get_review_likes(
    review_id: str,
    like_ugc_handler: LikeUgcHandler = Depends(get_review_like_ugc_service),
) -> JSONResponse:
    likes = await like_ugc_handler.find_ugc_content(target_id=review_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=likes)
