from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel, Field

from db_models.mongo_base_model import MongoBaseModel


class Like(BaseModel):
    user_id: str


class WatchProgress(BaseModel):
    progress: float = Field(default=0)


class UserSummaryAggregation(BaseModel):
    movie_id: str
    likes: List[Like]
    user_liked: bool
    watch_progress: WatchProgress


class AbstractSummaryAggregator(ABC):
    def __init__(self, mongo_model: MongoBaseModel):
        self.mongo_model = mongo_model

    @abstractmethod
    async def aggregate(self, user_id: str, page_number: int = 0, page_limit: int = 0) -> List[UserSummaryAggregation]:
        raise NotImplementedError


class BookmarkSummaryAggregator(AbstractSummaryAggregator):
    async def aggregate(self, user_id: str, page_number: int = 0, page_limit: int = 0) -> List[UserSummaryAggregation]:
        skip_amount = page_number * page_limit

        pipeline: List[Dict[str, Any]] = [
            {'$match': {'user_id': user_id}},
            {
                '$lookup': {
                    'from': 'likes',
                    'localField': 'movie_id',
                    'foreignField': 'movie_id',
                    'as': 'likes',
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
                    'likes': 1,
                    'user_liked': {'$in': [user_id, '$likes.user_id']},
                    'watch_progress': {'$ifNull': [{'$arrayElemAt': ['$watch_progress.progress', 0]}, 0]},
                },
            },
            {'$skip': skip_amount},
            {'$limit': page_limit},
        ]

        documents = await self.mongo_model.collection.aggregate(pipeline).to_list(length=None)
        return [UserSummaryAggregation(**doc) for doc in documents]
