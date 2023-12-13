from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from src.auxiliary_services.cache_service import CacheService
from src.auxiliary_services.data_aggregation import MovieDetailedAggregator, WatchProgressSummaryAggregator
from src.auxiliary_services.movie_search import MovieSearch
from src.core.settings import settings
from src.db_models.like import LikeModel
from src.db_models.watch_progress import WatchProgressModel
from src.dependencies.mongo import AsyncMongoClient, get_mongo_client
from src.dependencies.movie import get_movie_api
from src.dependencies.redis import get_redis
from src.external_api.movie import MovieApi


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
