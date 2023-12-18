from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.auxiliary_services.ugc_handler import ReviewUgcHandler
from src.db_models.review import ReviewDocument, ReviewModel
from src.dependencies.auth import get_user_from_request_state
from src.endpoint_services.review import get_review_model, get_review_ugc_service
from src.models.review import DeleteReview, ReviewContent
from src.models.user import User

router = APIRouter()


@router.post(
    '/{movie_id}',
    summary='Add review for movie',
)
async def add_review_to_movie(
    movie_id: str,
    review: ReviewContent,
    user: User = Depends(get_user_from_request_state),
    review_ugc_service: ReviewUgcHandler = Depends(get_review_ugc_service),
) -> JSONResponse:
    try:
        await review_ugc_service.add_ugc_content(target_id=movie_id, user_id=user.id, additional=review.review)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'detail': 'CREATED'})
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')


@router.delete(
    '/{movie_id}',
    summary='Delete review for movie',
)
async def delete_review_from_movie(
    review_body: DeleteReview,
    user: User = Depends(get_user_from_request_state),
    review_ugc_service: ReviewUgcHandler = Depends(get_review_ugc_service),
) -> JSONResponse:
    try:
        await review_ugc_service.delete_ugc_content(target_id=review_body.id, user_id=user.id)

        return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': 'Successfully deleted review'})
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')


@router.patch(
    '/update/{review_id}',
    summary='Update review for movie',
)
async def update_review_to_movie(
    review_id: str,
    review: ReviewContent,
    user: User = Depends(get_user_from_request_state),
    review_ugc_service: ReviewUgcHandler = Depends(get_review_ugc_service),
) -> JSONResponse:
    try:
        await review_ugc_service.update_ugc_content(review_id=review_id, user_id=user.id, additional=review.review)

        return JSONResponse(status_code=status.HTTP_200_OK, content={'detail': 'Successfully updated review'})
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')


@router.get(
    '/{movie_id}',
    summary='Get reviews for a movie',
)
async def get_reviews_for_movie(
    movie_id: str,
    collection: ReviewModel = Depends(get_review_model),
) -> List[ReviewDocument]:
    try:
        return await collection.get_reviews_by_movie(movie_id=movie_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')
