from typing import Annotated, List, Optional

from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from core.settings import settings
from endpoint_services.bookmark import get_bookmark_model, get_bookmark_service
from models.movie import MovieSummaryResponse
from models.user import User
from src.auxiliary_services.movie_search import MovieSearch
from src.db_models.bookmark import BookmarkModel
from src.dependencies.auth import get_user_from_request_state
from src.dependencies.kafka import get_kafka_producer

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
        'movie_id': movie_id,
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
        'movie_id': movie_id,
        'is_adding': False,
    }

    await kafka_producer.send(topic=settings.ugc_topic, key='bookmark', value=message_to_kafka)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'detail': 'DELETED'},
    )


@router.get(
    '/',
    summary="Get user's bookmarks",
)
async def get_bookmarks(
    page_size: Annotated[int, Query(description='Items on page', ge=1)] = 50,
    page_number: Annotated[int, Query(description='Page number', ge=0)] = 0,
    user: User = Depends(get_user_from_request_state),
    search: MovieSearch = Depends(get_bookmark_service),
) -> Optional[List[MovieSummaryResponse]]:
    return await search.get_user_movies(user_id=user.id, page_number=page_number, page_limit=page_size)
