"""Утилита для подготовки аутентифицированного пользователя."""
import logging
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from tests.functional.db import record
from tests.functional.models.auth.users import User
from tests.functional.settings import test_settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

ACCESS_TOKEN_LIFETIME = 60
REFRESH_TOKEN_LIFETIME = 60
ENCODING_ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def prepare_authenticated_user(auth_api_pg_session, redis_client, new_user):

    # Подготовка пользователя:

    # 1. "Регистрируем" пользователя:

    new_user['password'] = pwd_context.hash(new_user['password'])

    new_user_in_db = await record.add_record(pg_session=auth_api_pg_session, model=User, filler=new_user)

    # 2. Аутентифицируем его ("логиним"):
    token_content = {'subject': str(new_user_in_db.id)}

    access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    refresh_token_expires = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_LIFETIME)

    content_to_encode = token_content.copy()

    # 3. Создаём access token
    content_to_encode.update({'expires': access_token_expires.strftime('%m/%d/%Y, %H:%M:%S')})
    access_token = jwt.encode(
        content_to_encode,
        test_settings.SECRET_KEY,
        algorithm=ENCODING_ALGORITHM,
    )

    # 4. Создаём refresh token
    content_to_encode.update({'expires': refresh_token_expires.strftime('%m/%d/%Y, %H:%M:%S')})
    refresh_token = jwt.encode(
        content_to_encode,
        test_settings.SECRET_KEY_REFRESH,
        algorithm=ENCODING_ALGORITHM,
    )

    # 3. Сохраняем в кэш user_id по refresh токену
    await redis_client.set(
        refresh_token,
        content_to_encode['subject'],
        int(REFRESH_TOKEN_LIFETIME * 60),
    )
    return access_token, refresh_token, str(new_user_in_db.id)
