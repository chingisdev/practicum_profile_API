from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, AsyncGenerator, Callable

import aiohttp


@asynccontextmanager
async def aiohttp_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    async with aiohttp.ClientSession() as session:
        yield session


def with_aiohttp_session(func: Callable) -> Callable:
    """HOC for session management"""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async with aiohttp_session() as session:
            return await func(*args, session=session, **kwargs)
    return wrapper
