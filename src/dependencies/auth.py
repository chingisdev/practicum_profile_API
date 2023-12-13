from fastapi import Request

from src.core.settings import settings
from src.external_api.auth import AuthApi
from src.models.user import User

auth_api: AuthApi | None


def get_user_from_request_state(request: Request) -> User:
    authorized_user: User = User(
        id='2f384bd0-97a7-45e1-9f9f-da79affa8048',
        first_name='test',
        last_name='test',
        email='test',
        is_admin=True,
    )
    if settings.auth_enabled:
        authorized_user = request.state.user
    return authorized_user
