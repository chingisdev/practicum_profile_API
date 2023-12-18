import logging
from typing import Any, TypeVar

import uvicorn
from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from src.api.v1.bookmark import router as bookmark_router
from src.api.v1.like import router as like_router
from src.api.v1.movie import router as movie_router
from src.api.v1.review import router as review_router
from src.api.v1.user import router as user_router
from src.api.v1.watch_progress import router as progress_router
from src.core.exceptions import KafkaException, OtherException, UserDataException
from src.core.logger import LOGGING
from src.core.settings import settings
from src.dependencies import auth, kafka, mongo, movie, redis
from src.external_api.auth import AuthApi
from src.external_api.movie import MovieApi
from src.project_utilities.kafka_admin import ensure_topic_exists
from src.rate_limit.token_bucket import TokenBucket

app = FastAPI(
    title='Profile service',
    description='Provides information about the user.',
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    root_path='/profile',
    default_response_class=JSONResponse,
)
token_bucket = TokenBucket(
    rate=settings.token_bucket_rate, capacity=settings.token_bucket_capacity,
)


@app.on_event('startup')
async def startup() -> None:
    kafka.kafka_producer = AIOKafkaProducer(**settings.kafka_config)
    await kafka.kafka_producer.start()
    mongo.mongo_client = AsyncIOMotorClient(settings.mongo_database_url)
    redis.redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
    )
    auth.auth_api = AuthApi(base_url=settings.auth_user_endpoint)
    movie.movie_api = MovieApi(base_url=settings.movie_endpoint)


@app.on_event('shutdown')
async def shutdown() -> None:
    if kafka.kafka_producer:
        await kafka.kafka_producer.stop()


_T = TypeVar('_T', bound=Exception)


def exception_handler(request: Request, exc: _T):
    logging.error(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(KafkaException)
def kafka_exception_handler(request: Request, exc: KafkaException):
    return exception_handler(request, exc)


@app.exception_handler(UserDataException)
def user_data_exception_handler(request: Request, exc: UserDataException):
    return exception_handler(request, exc)


@app.exception_handler(OtherException)
def other_exception_handler(request: Request, exc: OtherException):
    return exception_handler(request, exc)


@app.middleware('http')
async def check_header_middleware(request: Request, call_next: Any) -> Any:
    if settings.production_mode:
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='X-Request-Id is required')
    return await call_next(request)


@app.middleware('http')
async def rate_limit_middleware(request: Request, call_next: Any) -> Any:
    if not token_bucket.is_available():
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail='Too many requests')
    return await call_next(request)


@app.middleware('http')
async def check_token_auth_middleware(request: Request, call_next: Any) -> Any:
    if settings.auth_enabled and request.url.path.startswith(settings.api_path):
        headers = {'Authorization': request.headers.get('Authorization')}
        if auth.auth_api:
            request.state.user = await auth.auth_api.validate_user(headers=headers)
        logging.info('Placed received user to request user')

    return await call_next(request)


app.include_router(like_router, prefix='/api/v1/like', tags=['Likes'])
app.include_router(review_router, prefix='/api/v1/review', tags=['Review'])
app.include_router(bookmark_router, prefix='/api/v1/bookmark', tags=['Bookmark'])
app.include_router(user_router, prefix='/api/v1/profile', tags=['Profile'])
app.include_router(movie_router, prefix='/api/v1/collection', tags=['Collection'])
app.include_router(progress_router, prefix='/api/v1/progress', tags=['Progress'])

if __name__ == '__main__':
    for topic in settings.kafka_topics:
        ensure_topic_exists(topic_name=topic, bootstrap_servers=settings.kafka_bootstrap_servers)

    uvicorn_default_port = 8000

    uvicorn.run(
        app,
        host='localhost',
        port=uvicorn_default_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
