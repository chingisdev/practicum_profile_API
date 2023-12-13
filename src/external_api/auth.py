import logging
from http import HTTPStatus
from typing import Dict, Optional

from aiohttp.client import ClientSession
from fastapi import HTTPException

from src.models.user import User
from src.utils.async_session import with_aiohttp_session
from src.utils.backoff import backoff_public_methods


@backoff_public_methods()
class AuthApi:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @with_aiohttp_session
    async def validate_user(self, session: ClientSession, headers: Dict[str, str]) -> Optional[User]:
        async with session.get(self.base_url, headers=headers) as response:
            logging.info('GOT RESPONSE FROM AUTH')

            if response.status == HTTPStatus.OK:
                logging.info('Got user data from auth service')
                user = await response.json()
                return User(**user)

            raise HTTPException(status_code=response.status, detail='Authentication Failed')
