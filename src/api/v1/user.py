from typing import Optional

from aiokafka import AIOKafkaProducer, KafkaError  # type: ignore
from fastapi import APIRouter, Depends, HTTPException, status

from src.core.exceptions import KafkaException
from src.core.settings import settings
from src.db_models.user import UserDocument, UserModel
from src.dependencies.auth import get_user_from_request_state
from src.dependencies.kafka import get_kafka_producer
from src.endpoint_services.user import get_user_model
from src.models.user import User, UserUpdate

router = APIRouter()


@router.patch(
    '/',
    summary='Update user information',
)
async def update_user_information(
    update_info: UserUpdate,
    user: User = Depends(get_user_from_request_state),
    collection: UserModel = Depends(get_user_model),
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> Optional[UserDocument]:
    try:
        await collection.update_user(user_id=user.id, update_data=update_info)

        message_to_kafka = {
            'user_id': user.id,
            'target_id': user.id,
            'is_adding': True,
            'additional': '',
        }
        await kafka_producer.send(topic=settings.ugc_topic, key='profile', value=message_to_kafka)

        return await collection.get_user(user_id=user.id)
    except KafkaError:
        raise KafkaException('Kafka error')
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')


@router.get(
    '/',
    summary='Get user information',
)
async def get_user_information(
    user: User = Depends(get_user_from_request_state),
    collection: UserModel = Depends(get_user_model),
) -> Optional[UserDocument]:
    try:
        return await collection.get_user(user_id=user.id)
    except KafkaError:
        raise KafkaException('Kafka error')
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')
