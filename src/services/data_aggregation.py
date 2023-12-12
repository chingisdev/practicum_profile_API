from abc import ABC, abstractmethod
from typing import Any, Dict, List

from models.movie import MovieDetailedAggregation, MovieSummaryAggregation
from src.db_models.like import LikeModel, TargetType
from src.db_models.mongo_base_model import MongoBaseModel


class AbstractSummaryAggregator(ABC):
    def __init__(self, mongo_model: MongoBaseModel):
        self.mongo_model = mongo_model

    @abstractmethod
    async def aggregate(self, user_id: str, page_number: int = 0, page_limit: int = 0) -> Any:
        raise NotImplementedError


class MovieDetailedAggregator:
    def __init__(self, like_model: LikeModel):
        self.like_model = like_model

    async def aggregate(self, user_id: str, movie_id: str) -> MovieDetailedAggregation:

        pipeline: List[Dict[str, Any]] = [
            {'$match': {'target_id': movie_id}},
            {
                '$lookup': {
                    'from': 'likes',
                    'localField': 'target_id',
                    'foreignField': 'target_id',
                    'as': 'likes_info',
                },
            },
            {
                '$lookup': {
                    'from': 'bookmarks',
                    'localField': 'target_id',
                    'foreignField': 'movie_id',
                    'as': 'bookmarks_info',
                },
            },
            {
                '$lookup': {
                    'from': 'watch_progress',
                    'let': {'movie_id': '$target_id', 'user_id': user_id},
                    'pipeline': [
                        {'$match': {
                            '$expr': {
                                '$and': [
                                    {'$eq': ['$movie_id', '$$movie_id']},
                                    {'$eq': ['$user_id', '$$user_id']},
                                ],
                            },
                        }},
                        {'$limit': 1},
                    ],
                    'as': 'watch_progress',
                },
            },
            {
                '$project': {
                    'movie_id': '$target_id',
                    'likes_count': {'$size': '$likes_info'},
                    'user_liked': {'$in': [user_id, '$likes_info.user_id']},
                    'bookmarks_count': {'$size': '$bookmarks_info'},
                    'user_bookmarked': {'$in': [user_id, '$bookmarks_info.user_id']},
                    'watch_progress': {'$ifNull': [{'$arrayElemAt': ['$watch_progress.progress', 0]}, 0]},
                },
            },
        ]
        documents = await self.like_model.collection.aggregate(pipeline).to_list(length=1)
        return MovieDetailedAggregation(**documents[0])


class BookmarkSummaryAggregator(AbstractSummaryAggregator):
    async def aggregate(self, user_id: str, page_number: int = 0, page_limit: int = 0) -> List[MovieSummaryAggregation]:
        skip_amount = page_number * page_limit

        pipeline: List[Dict[str, Any]] = [
            {'$match': {'user_id': user_id}},
            {'$skip': skip_amount},
            {'$limit': page_limit},
            {
                '$lookup': {
                    'from': 'likes',
                    'localField': 'movie_id',
                    'foreignField': 'target_id',
                    'as': 'likes_info',
                },
            },
            {
                '$lookup': {
                    'from': 'watch_progress',
                    'let': {'movie_id': '$movie_id', 'user_id': '$user_id'},
                    'pipeline': [
                        {'$match': {
                            '$expr': {
                                '$and': [
                                    {'$eq': ['$movie_id', '$$movie_id']},
                                    {'$eq': ['$user_id', '$$user_id']},
                                ],
                            },
                        },
                        },
                        {'$limit': 1},
                    ],
                    'as': 'watch_progress',
                },
            },
            {
                '$project': {
                    'movie_id': 1,
                    'likes_count': {'$size': '$likes_info'},
                    'user_liked': {'$in': [user_id, '$likes_info.user_id']},
                    'watch_progress': {'$ifNull': [{'$arrayElemAt': ['$watch_progress.progress', 0]}, 0]},
                },
            },
        ]

        documents = await self.mongo_model.collection.aggregate(pipeline).to_list(length=None)
        return [MovieSummaryAggregation(**doc) for doc in documents]


class LikesSummaryAggregator(AbstractSummaryAggregator):
    async def aggregate(self, user_id: str, page_number: int = 0, page_limit: int = 0) -> List[MovieSummaryAggregation]:
        skip_amount = page_number * page_limit

        pipeline: List[Dict[str, Any]] = [
            {'$match': {'user_id': user_id, 'target_type': TargetType.movie.value}},
            {'$skip': skip_amount},
            {'$limit': page_limit},
            {
                '$lookup': {
                    'from': 'likes',
                    'localField': 'target_id',
                    'foreignField': 'target_id',
                    'as': 'likes_info',
                },
            },
            {
                '$lookup': {
                    'from': 'watch_progress',
                    'let': {'movie_id': '$movie_id', 'user_id': '$user_id'},
                    'pipeline': [
                        {'$match': {
                            '$expr': {
                                '$and': [
                                    {'$eq': ['$movie_id', '$$movie_id']},
                                    {'$eq': ['$user_id', '$$user_id']},
                                ],
                            },
                        },
                        },
                        {'$limit': 1},
                    ],
                    'as': 'watch_progress',
                },
            },
            {
                '$project': {
                    'movie_id': '$target_id',
                    'likes_count': {'$size': '$likes_info'},
                    'user_liked': True,
                    'watch_progress': {'$ifNull': [{'$arrayElemAt': ['$watch_progress.progress', 0]}, 0]},
                },
            },
        ]

        documents = await self.mongo_model.collection.aggregate(pipeline).to_list(length=None)
        return [MovieSummaryAggregation(**doc) for doc in documents]


class WatchProgressSummaryAggregator(AbstractSummaryAggregator):
    async def aggregate(self, user_id: str, page_number: int = 0, page_limit: int = 0) -> List[MovieSummaryAggregation]:
        skip_amount = page_number * page_limit

        pipeline: List[Dict[str, Any]] = [
            {'$match': {'user_id': user_id}},
            {'$skip': skip_amount},
            {'$limit': page_limit},
            {
                '$lookup': {
                    'from': 'likes',
                    'localField': 'movie_id',
                    'foreignField': 'target_id',
                    'as': 'likes_info',
                },
            },
            {
                '$project': {
                    'movie_id': '$target_id',
                    'likes_count': {'$size': '$likes_info'},
                    'user_liked': {'$in': [user_id, '$likes_info.user_id']},
                    'watch_progress': '$progress',
                },
            },
        ]

        documents = await self.mongo_model.collection.aggregate(pipeline).to_list(length=None)
        return [MovieSummaryAggregation(**doc) for doc in documents]
