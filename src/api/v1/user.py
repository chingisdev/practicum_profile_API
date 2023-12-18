from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from src.db_models.user import UserDocument, UserModel
from src.dependencies.auth import get_user_from_request_state
from src.endpoint_services.user import UserUgcHandler, get_user_model, get_user_ugc_service
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
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong')
