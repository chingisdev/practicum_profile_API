from functools import lru_cache

from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import Depends
from redis.asyncio import Redis

from src.auxiliary_services.cache_service import CacheService
from src.auxiliary_services.data_aggregation import BookmarkSummaryAggregator, MovieDetailedAggregator
from src.auxiliary_services.message_broker import KafkaAsyncMessageBroker
from src.auxiliary_services.movie_search import MovieSearch
from src.auxiliary_services.ugc_handler import ReviewUgcHandler
from src.core.settings import settings
from src.db_models.like import LikeModel
from src.db_models.review import ReviewModel
from src.dependencies.kafka import get_kafka_producer
from src.dependencies.mongo import AsyncMongoClient, get_mongo_client
from src.dependencies.movie import get_movie_api
from src.dependencies.redis import get_redis
from src.external_api.movie import MovieApi


@lru_cache()
def get_review_service(
    client: AsyncMongoClient = Depends(get_mongo_client),
    redis: Redis = Depends(get_redis),
    movie_api: MovieApi = Depends(get_movie_api),
) -> MovieSearch:
    db = client[settings.mongo_database]
    like_model = LikeModel(db)
    review_model = ReviewModel(db)
    cache_expire_time = 60 * 60 * 24 * 7
    cache_service = CacheService(redis_client=redis, ttl=cache_expire_time)
    detailed_aggregator = MovieDetailedAggregator(like_model=like_model)
    summary_aggregator = BookmarkSummaryAggregator(mongo_model=review_model)
    return MovieSearch(
        cache=cache_service,
        detailed_aggregator=detailed_aggregator,
        summary_aggregator=summary_aggregator,
        movie_api=movie_api,
    )


@lru_cache()
def get_review_model(
    client: AsyncMongoClient = Depends(get_mongo_client),
) -> ReviewModel:
    db = client[settings.mongo_database]
    return ReviewModel(db)


@lru_cache()
def get_review_ugc_service(
    model: ReviewModel = Depends(get_review_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> ReviewUgcHandler:
    message_broker = KafkaAsyncMessageBroker(producer=kafka_producer, topic=settings.ugc_topic)
    return ReviewUgcHandler(collection=model, message_broker=message_broker)
