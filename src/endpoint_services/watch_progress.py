from functools import lru_cache

from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import Depends
from redis.asyncio import Redis

from src.auxiliary_services.cache_service import CacheService
from src.auxiliary_services.data_aggregation import MovieDetailedAggregator, WatchProgressSummaryAggregator
from src.auxiliary_services.message_broker import AsyncMessageBroker, KafkaAsyncMessageBroker
from src.auxiliary_services.movie_search import MovieSearch
from src.core.settings import settings
from src.db_models.like import LikeModel
from src.db_models.watch_progress import WatchProgressModel
from src.dependencies.kafka import get_kafka_producer
from src.dependencies.mongo import AsyncMongoClient, get_mongo_client
from src.dependencies.movie import get_movie_api
from src.dependencies.redis import get_redis
from src.external_api.movie import MovieApi
from src.models.movie_progress import MovieProgress
from src.models.user import User


class WatchProgressUgcHandler:
    def __init__(self, collection: WatchProgressModel, message_broker: AsyncMessageBroker):
        self.collection = collection
        self.message_broker = message_broker

    async def update(self, movie_progress: MovieProgress, user: User) -> None:
        await self.collection.update_progress(
            user_id=user.id,
            movie_id=movie_progress.id,
            break_point=movie_progress.break_point,
        )
        combined_data = {'movie': movie_progress.model_dump(), 'user': user.model_dump()}
        key = '{movie}+{user}'.format(movie=movie_progress.id, user=user.id)
        await self.message_broker.send(key=key, message=combined_data)


@lru_cache()
def get_watch_progress_service(
    client: AsyncMongoClient = Depends(get_mongo_client),
    redis: Redis = Depends(get_redis),
    movie_api: MovieApi = Depends(get_movie_api),
) -> MovieSearch:
    db = client[settings.mongo_database]
    like_model = LikeModel(db)
    watch_progress_model = WatchProgressModel(db)
    cache_expire_time = 60 * 60 * 24 * 7
    cache_service = CacheService(redis_client=redis, ttl=cache_expire_time)
    detailed_aggregator = MovieDetailedAggregator(like_model=like_model)
    summary_aggregator = WatchProgressSummaryAggregator(mongo_model=watch_progress_model)
    return MovieSearch(
        cache=cache_service,
        detailed_aggregator=detailed_aggregator,
        summary_aggregator=summary_aggregator,
        movie_api=movie_api,
    )


@lru_cache()
def get_watch_progress_model(
    client: AsyncMongoClient = Depends(get_mongo_client),
) -> WatchProgressModel:
    db = client[settings.mongo_database]
    return WatchProgressModel(db)


@lru_cache()
def get_watch_progress_ugc_service(
    model: WatchProgressModel = Depends(get_watch_progress_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> WatchProgressUgcHandler:
    message_broker = KafkaAsyncMessageBroker(producer=kafka_producer, topic=settings.watch_progress_topic)
    return WatchProgressUgcHandler(collection=model, message_broker=message_broker)
