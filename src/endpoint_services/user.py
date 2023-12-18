from functools import lru_cache
from typing import Optional

from aiokafka import AIOKafkaProducer  # type: ignore
from fastapi import Depends

from src.auxiliary_services.message_broker import AsyncMessageBroker, KafkaAsyncMessageBroker
from src.core.settings import settings
from src.db_models.user import UserDocument, UserModel
from src.dependencies.kafka import get_kafka_producer
from src.dependencies.mongo import AsyncMongoClient, get_mongo_client
from src.models.user import UserUpdate


class UserUgcHandler:
    key = 'user'

    def __init__(self, collection: UserModel, message_broker: AsyncMessageBroker):
        self.collection = collection
        self.message_broker = message_broker

    async def update_user(self, user_id: str, update_info: UserUpdate) -> Optional[UserDocument]:
        await self.collection.update_user(user_id=user_id, update_data=update_info)

        message_to_kafka = {
            'user_id': user_id,
            'target_id': user_id,
            'is_adding': True,
            'additional': '',
        }
        await self.message_broker.send(key=self.key, message=message_to_kafka)

        return await self.collection.get_user(user_id=user_id)


@lru_cache()
def get_user_model(
    client: AsyncMongoClient = Depends(get_mongo_client),
) -> UserModel:
    db = client[settings.mongo_database]
    return UserModel(db)


@lru_cache()
def get_user_ugc_service(
    model: UserModel = Depends(get_user_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> UserUgcHandler:
    message_broker = KafkaAsyncMessageBroker(producer=kafka_producer, topic=settings.ugc_topic)
    return UserUgcHandler(collection=model, message_broker=message_broker)
