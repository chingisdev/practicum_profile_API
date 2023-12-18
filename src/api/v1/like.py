from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auxiliary_services.ugc_handler import LikeUgcHandler
from src.db_models.like import LikeModel
from src.dependencies.auth import get_user_from_request_state
from src.endpoint_services.like import get_like_model, get_movie_like_ugc_service, get_review_like_ugc_service
from src.models.user import User

router = APIRouter()


@router.post(
    '/movie/{movie_id}',
    summary="User's like for movie",
    description="Accepts of user's likes.",
)
async def like_movie(
    movie_id: str,
    user: User = Depends(get_user_from_request_state),
    like_ugc_handler: LikeUgcHandler = Depends(get_movie_like_ugc_service),
) -> JSONResponse:
    try:
        await like_ugc_handler.add_ugc_content(target_id=movie_id, user_id=user.id)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'CREATED'})

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': 'Internal server error'},
        )


@router.delete(
    '/movie/{movie_id}',
    summary="User's dislike for movie",
    description="Accepts of user's dislike.",
)
async def dislike_movie(
    movie_id: str,
    user: User = Depends(get_user_from_request_state),
    like_ugc_handler: LikeUgcHandler = Depends(get_movie_like_ugc_service),
) -> JSONResponse:
    try:
        await like_ugc_handler.delete_ugc_content(target_id=movie_id, user_id=user.id)

        return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': 'DELETED'})

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': 'Internal server error'},
        )


@router.post(
    '/review/{review_id}',
    summary="User's like for review",
    description="Accepts of user's likes.",
)
async def like_review(
    review_id: str,
    user: User = Depends(get_user_from_request_state),
    like_ugc_handler: LikeUgcHandler = Depends(get_review_like_ugc_service),
) -> JSONResponse:
    try:
        await like_ugc_handler.add_ugc_content(target_id=review_id, user_id=user.id)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'CREATED'})

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': 'Internal server error'},
        )


@router.delete(
    '/review/{review_id}',
    summary="Remove user's like or unlike from review rating",
)
async def unlike_review(
    review_id: str,
    user: User = Depends(get_user_from_request_state),
    like_ugc_handler: LikeUgcHandler = Depends(get_review_like_ugc_service),
) -> JSONResponse:
    try:
        await like_ugc_handler.delete_ugc_content(target_id=review_id, user_id=user.id)

        return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': 'DELETED'})

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': 'Internal server error'},
        )


@router.get(
    '/movie/{movie_id}',
    summary='Users likes for movies',
    description='Likes values for movie.',
)
async def get_movie_likes(
    movie_id: str,
    collection: LikeModel = Depends(get_like_model),
) -> JSONResponse:
    try:
        likes = await collection.find({'target_id': movie_id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=likes)
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': 'Internal server error'},
        )


@router.get(
    '/review/{review_id}',
    summary='Users like for reviews',
    description='Like values for a review.',
)
async def get_review_likes(
    review_id: str,
    collection: LikeModel = Depends(get_like_model),
) -> JSONResponse:
    try:
        likes = await collection.find({'target_id': review_id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=likes)
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': 'Internal server error'},
        )
