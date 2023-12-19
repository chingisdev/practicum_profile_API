from aiokafka.errors import KafkaError
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auxiliary_services.ugc_handler import BookmarkUgcHandler
from src.core.exceptions import KafkaException, UserDataException
from src.dependencies.auth import get_user_from_request_state
from src.endpoint_services.bookmark import get_bookmark_ugc_service
from src.models.user import User

router = APIRouter()


@router.post(
    '/{movie_id}',
    summary='Create bookmark',
)
async def add_bookmark(
    movie_id: str,
    user: User = Depends(get_user_from_request_state),
    bookmark_ugc_handler: BookmarkUgcHandler = Depends(get_bookmark_ugc_service),
) -> JSONResponse:
    try:
        await bookmark_ugc_handler.add_ugc_content(target_id=movie_id, user_id=user.id)
    except InvalidId:
        raise UserDataException('Movie id is not valid')
    except KafkaError:
        raise KafkaException('Kafka error')

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
    bookmark_ugc_handler: BookmarkUgcHandler = Depends(get_bookmark_ugc_service),
) -> JSONResponse:
    try:
        await bookmark_ugc_handler.delete_ugc_content(target_id=movie_id, user_id=user.id)
    except InvalidId:
        raise UserDataException('Movie id is not valid')
    except KafkaError:
        raise KafkaException('Kafka error')

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'detail': 'DELETED'},
    )
