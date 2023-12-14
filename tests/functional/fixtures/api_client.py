"""Фикстуры клиента api и фабрики запросов к api."""
import logging
from dataclasses import dataclass
from typing import Optional

import aiohttp
import pytest_asyncio
from multidict import CIMultiDictProxy

from tests.scheduler_api_tests.settings import test_settings

logger = logging.getLogger(__name__)


@dataclass
class HTTPResponse:
    """Класс ответа от API."""

    body: dict  # тело ответа - значение response.json()

    # Из справки по aiohttp:
    # Response object
    # headers
    # A case-insensitive multidict proxy with HTTP headers of response,
    # CIMultiDictProxy.
    headers: CIMultiDictProxy[str]

    status: int


@pytest_asyncio.fixture(scope='session')
async def api_client_session():
    """Получить экземпляр сессии клиента API.

    Yields:
        api_client_session: сессия API
    """
    api_session = aiohttp.ClientSession()
    yield api_session
    await api_session.close()


# Из теории:
# Если необходимо передать функцию, которую нужно будет вызывать
# в коде и при этом вызвать другие фикстуры, воспользуйтесь возвратом вложенной
# функции:


@pytest_asyncio.fixture(scope='session')
def make_api_request(api_client_session):  # noqa: WPS442 аргумент должен
    # совпадать с фикстурой
    """Подготовить сопрограмму http запроса к тестируемому API.

    Args:
        api_client_session: экземпляр сессии клиента aiohttp

    Returns:
        inner: сопрограмма http запроса к тестируемому API

    """
    async def inner(  # noqa: WPS430 здесь необходимо использовать вложенную
        # функцию
        method: str,
        resource: str,
        postfix: Optional[str] = None,
        pk: Optional[str] = None,
        request_params: Optional[dict] = None,
        header: Optional[dict[str, str]] = None,
        form_data: Optional[dict[str, str]] = None,
        body: Optional[dict] = None,
    ) -> HTTPResponse:
        request_params = request_params or {}

        endpoint_url = '{service_url}/api/v1/{resource}'.format(
            service_url=test_settings.service_url,
            resource=resource,
        )
        if postfix is not None:
            endpoint_url = '{basic_url}/{postfix}'.format(
                basic_url=endpoint_url,
                postfix=postfix,
            )
        if pk is not None:
            endpoint_url = '{basic_url}/{pk}'.format(
                basic_url=endpoint_url,
                pk=pk,
            )

        async with api_client_session.request(
            method=method,
            url=endpoint_url,
            params=request_params,
            headers=header,
            data=form_data,
            json=body,
        ) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return HTTPResponse(
                body=body,
                headers=headers,
                status=status,
            )

    return inner
