from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.core.settings import settings
from src.db_models.like import LikeDocument, LikeModel, TargetType
from src.dependencies.auth import get_user_from_request_state
from src.dependencies.kafka import get_kafka_producer
from src.endpoint_services.like import get_like_model
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
    collection: LikeModel = Depends(get_like_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> JSONResponse:
    try:
        like_document = LikeDocument(target_id=movie_id, user_id=user.id, target_type=TargetType.movie)
        await collection.add_like(like_document)

        message_to_kafka = {
            'user_id': user.id,
            'target_id': movie_id,
            'is_adding': True,
        }
        await kafka_producer.send(topic=settings.ugc_topic, key='movie-like', value=message_to_kafka)

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
    collection: LikeModel = Depends(get_like_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> JSONResponse:
    try:
        like_document = LikeDocument(target_id=movie_id, user_id=user.id, target_type=TargetType.movie)
        await collection.remove_like(like_document)

        message_to_kafka = {
            'user_id': user.id,
            'target_id': movie_id,
            'is_adding': False,
        }
        await kafka_producer.send(topic=settings.ugc_topic, key='movie-like', value=message_to_kafka)

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
    collection: LikeModel = Depends(get_like_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> JSONResponse:
    try:
        like_document = LikeDocument(target_id=review_id, user_id=user.id, target_type=TargetType.review)
        await collection.add_like(like_document)

        message_to_kafka = {
            'user_id': user.id,
            'target_id': review_id,
            'is_adding': True,
        }
        await kafka_producer.send(topic=settings.ugc_topic, key='review-like', value=message_to_kafka)

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
    collection: LikeModel = Depends(get_like_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> JSONResponse:
    try:
        like_document = LikeDocument(target_id=review_id, user_id=user.id, target_type=TargetType.review)
        await collection.remove_like(like_document)

        message_to_kafka = {
            'user_id': user.id,
            'target_id': review_id,
            'is_adding': False,
        }
        await kafka_producer.send(topic=settings.ugc_topic, key='review-like', value=message_to_kafka)

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
