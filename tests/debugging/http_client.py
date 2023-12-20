from dataclasses import dataclass
from typing import Optional

import aiohttp
from multidict import CIMultiDictProxy


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


async def make_request(  # noqa: WPS430 здесь необходимо использовать вложенную функцию
    method: str,
    endpoint_url: str,
    request_params: Optional[dict] = None,
    header: Optional[dict[str, str]] = None,
    form_data: Optional[dict[str, str]] = None,
    body: Optional[dict] = None,
) -> HTTPResponse:
    request_params = request_params or {}

    async with aiohttp.ClientSession() as api_client_session:
        async with api_client_session.request(
            method=method,
            url=endpoint_url,
            params=request_params,
            headers=header,
            data=form_data,
            json=body,
        ) as response:
            if response.status == 200:
                body = await response.json()
            else:
                body = {'msg': response.content}
            headers = response.headers
            status = response.status
            return HTTPResponse(
                body=body,
                headers=headers,
                status=status,
            )
