from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.core.settings import settings
from src.db_models.watch_progress import WatchProgressModel
from src.dependencies.auth import get_user_from_request_state
from src.dependencies.kafka import get_kafka_producer
from src.endpoint_services.watch_progress import get_watch_progress_model
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
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
    collection: WatchProgressModel = Depends(get_watch_progress_model),
) -> JSONResponse:
    try:
        await collection.update_progress(user_id=user.id, movie_id=movie.id, break_point=movie.break_point)
        combined_data = {'movie': movie.model_dump(), 'user': user.model_dump()}
        key = '{movie}+{user}'.format(movie=movie.id, user=user.id)
        await kafka_producer.send(
            topic=settings.watch_progress_topic, key=key, value=combined_data,
        )

        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={'detail': "User's watch progress has been saved"},
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')
