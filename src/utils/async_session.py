from functools import wraps
from typing import Any, Callable, Type

import aiohttp


def with_session(method: Callable) -> Callable:
    """HOC for session management"""

    @wraps(method)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        async with aiohttp.ClientSession() as session:
            return await method(self, session, *args, **kwargs)
    return wrapper


def async_session_for_public_methods() -> Callable:
    """Context manager for API classes"""

    def decorator(cls: Type[object]) -> Type[object]:
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                setattr(cls, attr_name, with_session(attr_value))
        return cls
    return decorator
