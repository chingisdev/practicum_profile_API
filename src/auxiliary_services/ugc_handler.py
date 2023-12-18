from abc import ABC, abstractmethod

from fastapi import HTTPException, status

from src.auxiliary_services.message_broker import AsyncMessageBroker
from src.db_models.bookmark import BookmarkModel
from src.db_models.like import LikeDocument, LikeModel, TargetType
from src.db_models.review import ReviewModel


class UgcHandler(ABC):
    def __init__(self, message_broker: AsyncMessageBroker):
        self.message_broker = message_broker

    @abstractmethod
    async def add_ugc_content(self, target_id: str, user_id: str, additional: str | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_ugc_content(self, target_id: str, user_id: str, additional: str | None = None) -> None:
        raise NotImplementedError


class BookmarkUgcHandler(UgcHandler):
    key = 'bookmark'

    def __init__(self, collection: BookmarkModel, message_broker: AsyncMessageBroker):
        self.collection = collection
        super().__init__(message_broker)

    async def add_ugc_content(self, target_id: str, user_id: str, additional: str | None = None) -> None:
        await self.collection.add_bookmark(user_id=user_id, movie_id=target_id)

        message_to_send = {
            'user_id': user_id,
            'target_id': target_id,
            'is_adding': True,
        }

        await self.message_broker.send(key=self.key, message=message_to_send)

    async def delete_ugc_content(self, target_id: str, user_id: str, additional: str | None = None) -> None:
        await self.collection.remove_bookmark(user_id=user_id, movie_id=target_id)

        message_to_send = {
            'user_id': user_id,
            'target_id': target_id,
            'is_adding': False,
        }

        await self.message_broker.send(key=self.key, message=message_to_send)


class LikeUgcHandler(UgcHandler):
    key = 'like'

    def __init__(self, collection: LikeModel, message_broker: AsyncMessageBroker, target_type: TargetType):
        super().__init__(message_broker)
        self.collection = collection
        self.target_type = target_type

    async def add_ugc_content(self, target_id: str, user_id: str, additional: str | None = None) -> None:
        like_document = LikeDocument(target_id=target_id, user_id=user_id, target_type=self.target_type)
        await self.collection.add_like(like_document)

        message_to_send = {
            'user_id': user_id,
            'target_id': target_id,
            'is_adding': True,
        }
        await self.message_broker.send(key=self.key, message=message_to_send)

    async def delete_ugc_content(self, target_id: str, user_id: str, additional: str | None = None) -> None:
        like_document = LikeDocument(target_id=target_id, user_id=user_id, target_type=self.target_type)
        await self.collection.remove_like(like_document)

        message_to_send = {
            'user_id': user_id,
            'target_id': target_id,
            'is_adding': False,
        }
        await self.message_broker.send(key=self.key, message=message_to_send)


class ReviewUgcHandler(UgcHandler):
    key = 'review'

    def __init__(self, collection: ReviewModel, message_broker: AsyncMessageBroker):
        super().__init__(message_broker)
        self.collection = collection

    async def add_ugc_content(self, target_id: str, user_id: str, additional: str | None = None) -> None:
        if additional is None:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='text of review cannot be empty')

        review_result = await self.collection.add_review(user_id=user_id, movie_id=target_id, review=additional)

        message_to_send = {
            'user_id': user_id,
            'target_id': review_result.id,
            'is_adding': True,
            'additional': additional,
        }
        await self.message_broker.send(key=self.key, message=message_to_send)

    async def delete_ugc_content(self, target_id: str, user_id: str, additional: str | None = None) -> None:
        await self.collection.remove_review(review_id=target_id)

        message_to_send = {
            'user_id': user_id,
            'target_id': target_id,
            'is_adding': False,
            'additional': additional,
        }
        await self.message_broker.send(key=self.key, message=message_to_send)

    async def update_ugc_content(self, review_id: str, user_id: str, additional: str | None) -> None:
        if additional is None:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='text of review cannot be empty')

        review_update_status = await self.collection.update_review(
            review_id=review_id,
            user_id=user_id,
            new_review_content=additional,
        )
        if not review_update_status:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the author of review')

        message_to_send = {
            'user_id': user_id,
            'target_id': review_id,
            'is_adding': True,
            'additional': additional,
        }
        await self.message_broker.send(key=self.key, message=message_to_send)
