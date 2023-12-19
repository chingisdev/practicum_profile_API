from typing import Optional

from aiokafka.errors import KafkaError
from bson.errors import InvalidId
from fastapi import APIRouter, Depends

from src.core.exceptions import KafkaException, OtherException, UserDataException
from src.db_models.user import UserDocument
from src.dependencies.auth import get_user_from_request_state
from src.endpoint_services.user import UserUgcHandler, get_user_ugc_service
from src.models.user import User, UserUpdate

router = APIRouter()


@router.patch(
    '/',
    summary='Update user information',
)
async def update_user_information(
    update_info: UserUpdate,
    user: User = Depends(get_user_from_request_state),
    user_ugc_service: UserUgcHandler = Depends(get_user_ugc_service),
) -> Optional[UserDocument]:
    try:
        return await user_ugc_service.update_user(user_id=user.id, update_info=update_info)
    except InvalidId:
        raise UserDataException('User id is not valid')
    except KafkaError:
        raise KafkaException('Kafka error')
    except Exception as e:
        raise OtherException(f'{e.__class__.__name__} - {e.args[0]}')


@router.get(
    '/',
    summary='Get user information',
)
async def get_user_information(
    user: User = Depends(get_user_from_request_state),
    user_ugc_service: UserUgcHandler = Depends(get_user_ugc_service),
) -> Optional[UserDocument]:
    try:
        return await user_ugc_service.get_user(user_id=user.id)
    except InvalidId:
        raise UserDataException('User id is not valid')
    except Exception as e:
        raise OtherException(f'{e.__class__.__name__} - {e.args[0]}')
