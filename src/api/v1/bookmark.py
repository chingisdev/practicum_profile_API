from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from core.settings import settings
from models.user import User
from src.db_models.bookmark import BookmarkModel
from src.dependencies.auth import get_user_from_request_state
from src.dependencies.kafka import get_kafka_producer
from src.endpoint_services.bookmark import get_bookmark_model

router = APIRouter()


@router.post(
    '/{movie_id}',
    summary='Create bookmark',
)
async def add_bookmark(
    movie_id: str,
    user: User = Depends(get_user_from_request_state),
    collection: BookmarkModel = Depends(get_bookmark_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> JSONResponse:
    await collection.add_bookmark(user_id=user.id, movie_id=movie_id)

    message_to_kafka = {
        'user_id': user.id,
        'target_id': movie_id,
        'is_adding': True,
    }

    await kafka_producer.send(topic=settings.ugc_topic, key='bookmark', value=message_to_kafka)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'detail': 'CREATED'},
    )


@router.delete(
    '/{movie_id}',
    summary='Delete bookmark',
)
async def remove_bookmark(
    movie_id: str,
    user: User = Depends(get_user_from_request_state),
    collection: BookmarkModel = Depends(get_bookmark_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> JSONResponse:
    await collection.remove_bookmark(user_id=user.id, movie_id=movie_id)

    message_to_kafka = {
        'user_id': user.id,
        'target_id': movie_id,
        'is_adding': False,
    }

    await kafka_producer.send(topic=settings.ugc_topic, key='bookmark', value=message_to_kafka)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'detail': 'DELETED'},
    )
