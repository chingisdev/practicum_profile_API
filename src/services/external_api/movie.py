from http import HTTPStatus
from typing import Dict, List, Optional

from aiohttp.client import ClientSession

from utils.async_session import async_session_for_public_methods
from utils.backoff import backoff_public_methods


@backoff_public_methods()
@async_session_for_public_methods()
class MovieApi:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_several(self, session: ClientSession, movie_ids: List[str]) -> List[Optional[Dict]]:
        """Fetch details for multiple movies by their IDs."""

        ids_param = ', '.join(movie_ids)
        url = '{url}/movies?ids={ids}'.format(url=self.base_url, ids=ids_param)
        async with session.get(url) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()
            return []
