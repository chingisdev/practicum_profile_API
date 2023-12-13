from typing import List, Optional

from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.core.settings import settings
from src.db_models.review import ReviewDocument, ReviewModel
from src.dependencies.auth import get_user_from_request_state
from src.dependencies.kafka import get_kafka_producer
from src.endpoint_services.review import get_review_model
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
    collection: ReviewModel = Depends(get_review_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> ReviewDocument:
    try:
        review_result = await collection.add_review(user_id=user.id, movie_id=movie_id, review=review)

        message_to_kafka = {
            'user_id': user.id,
            'target_id': review_result.id,
            'is_adding': True,
            'additional': review_result.review,
        }
        await kafka_producer.send(topic=settings.ugc_topic, key='review', value=message_to_kafka)

        return review_result
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')


async def check_if_exist(review: Optional[ReviewDocument]) -> None:
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review doesn't exist")


async def check_authority(review: Optional[ReviewDocument], user_id: str) -> None:
    if review and review.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the author of review')


@router.delete(
    '/delete-review',
    summary='Delete review for movie',
)
async def delete_review_from_movie(
    review_body: DeleteReview,
    user: User = Depends(get_user_from_request_state),
    collection: ReviewModel = Depends(get_review_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> JSONResponse:
    try:
        review = await collection.find_one({'_id': review_body.id})
        await check_if_exist(review)
        await check_authority(review, user.id)
        await collection.remove_review(review_id=review_body.id)

        message_to_kafka = {
            'user_id': user.id,
            'target_id': review_body.id,
            'is_adding': False,
            'additional': '',
        }
        await kafka_producer.send(topic=settings.ugc_topic, key='review', value=message_to_kafka)

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
    collection: ReviewModel = Depends(get_review_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> JSONResponse:
    try:
        review_update_status = await collection.update_review(
            review_id=review_id,
            user_id=user.id,
            new_review_content=review,
        )
        if not review_update_status:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the author of review')

        message_to_kafka = {
            'user_id': user.id,
            'target_id': review_id,
            'is_adding': True,
            'additional': review.review,
        }
        await kafka_producer.send(topic=settings.ugc_topic, key='review', value=message_to_kafka)

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
