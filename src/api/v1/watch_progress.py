from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from dependencies.kafka import get_kafka_producer
from models.movie_progress import MovieProgress
from src.endpoint_services.watch_progress import get_watch_progress_model
from src.db_models.watch_progress import WatchProgressModel
from models.user import User
from aiokafka import AIOKafkaProducer
from src.dependencies.auth import get_user_from_request_state
from core.settings import settings

router = APIRouter()


@router.post(
    "/",
    summary="User's watching progress",
    description="Accepts checkpoints of user's watching progress.",
)
async def handle_user_view_progress(
    movie: MovieProgress,
    user: User = Depends(get_user_from_request_state),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
    collection: WatchProgressModel = Depends(get_watch_progress_model)
):
    try:
        await collection.update_progress(user_id=user.id, movie_id=movie.id, break_point=movie.break_point)
        combined_data = {"movie": movie.model_dump(), "user": user.model_dump()}
        key = f"{movie.id}+{user.id}"
        await kafka_producer.send(
            topic=settings.watch_progress_topic, key=key, value=combined_data
        )

        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"detail": "User's watch progress has been saved"},
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
