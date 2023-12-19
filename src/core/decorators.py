import logging
from functools import wraps

from aiokafka.errors import KafkaError
from bson.errors import InvalidId

from src.core.exceptions import KafkaException, OtherException, UserDataException

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def catch_broker_exceptions(func):
    """Отлавливание исключений брокера."""
    @wraps(func)
    async def catch_broker_exceptions_wrapper(
        *args,
        **kwargs,
    ) -> None:
        try:
            return await func(*args, **kwargs)
        except KafkaError:
            raise KafkaException('Kafka error')
        except Exception as e:
            raise OtherException(f'{e.__class__.__name__} - {e.args[0]}')
    return catch_broker_exceptions_wrapper


def catch_collection_exceptions(func):
    """Отлавливание исключений получения данных."""
    @wraps(func)
    async def catch_collection_exceptions_wrapper(
        *args,
        **kwargs,
    ) -> None:
        try:
            return await func(*args, **kwargs)
        except InvalidId:
            raise UserDataException('User id is not valid')
        except Exception as e:
            raise OtherException(f'{e.__class__.__name__} - {e.args[0]}')
    return catch_collection_exceptions_wrapper


def catch_collection_broker_exceptions(func):
    """Отлавливание исключений получения данных."""
    @wraps(func)
    async def catch_collection_broker_exceptions_wrapper(
        *args,
        **kwargs,
    ) -> None:
        try:
            return await func(*args, **kwargs)
        except InvalidId:
            raise UserDataException('User id is not valid')
        except KafkaError:
            raise KafkaException('Kafka error')
        except Exception as e:
            raise OtherException(f'{e.__class__.__name__} - {e.args[0]}')
    return catch_collection_broker_exceptions_wrapper
