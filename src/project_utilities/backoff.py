import logging
from typing import Callable, Type

from tenacity import before_sleep_log, retry, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def backoff(wait_multiplier: int = 1, wait_minimum: int = 4, wait_maximum: int = 10) -> Callable:
    """
    Wrap input function with exponential backoff retry logic.

    Args:
        wait_multiplier (int): Multiplier for exponential backoff. Default is 1.
        wait_minimum (int): Minimum wait time for exponential backoff. Default is 4.
        wait_maximum (int): Maximum wait time for exponential backoff. Default is 10.

    Returns:
        Callable: A decorator function that, when applied to a function,
                  adds retry logic with exponential backoff to that function.
    """

    def decorator(func: Callable) -> Callable:
        return retry(
            wait=wait_exponential(multiplier=wait_multiplier, min=wait_minimum, max=wait_maximum),
            before_sleep=before_sleep_log(logger, logging.INFO),
        )(func)

    return decorator


def backoff_public_methods(wait_multiplier: int = 1, wait_minimum: int = 4, wait_maximum: int = 10) -> Callable:
    """
        Decorate all public methods of a class with backoff decorator.

        Args:
            wait_multiplier (int): Multiplier for exponential backoff. Default is 1.
            wait_minimum (int): Minimum wait time for exponential backoff. Default is 4.
            wait_maximum (int): Maximum wait time for exponential backoff. Default is 10.

        Returns:
            Callable: A decorator function that, when applied to a class,
                      adds retry logic with exponential backoff to all public methods of the class.
        """

    def decorator(cls: Type[object]) -> Type[object]:
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                setattr(cls, attr_name, backoff(wait_multiplier, wait_minimum, wait_maximum)(attr_value))
        return cls

    return decorator
