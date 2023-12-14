from http import HTTPStatus
from typing import List, Optional

from aiohttp.client import ClientSession

from src.models.movie import MovieApiResponse, MovieGenre, MoviePerson, MoviePersonName
from src.project_utilities.async_session import with_aiohttp_session
from src.project_utilities.backoff import backoff_public_methods


def deserialize_movie_json(film: dict) -> 'MovieApiResponse':
    return MovieApiResponse(
        id=film['id'],
        title=film['title'],
        description=film['description'],
        imdb_rating=film['imdb_rating'],
        actors=[
            MoviePerson(
                id=person['id'],
                full_name=person['full_name'],
            )
            for person in film['actors']
            if person is not None
        ],
        writers=[
            MoviePerson(
                id=person['id'],
                full_name=person['full_name'],
            )
            for person in film['writers']
            if person is not None
        ],
        directors=[
            MoviePersonName(full_name=director['full_name'])
            for director in film['directors']
            if director is not None
        ],
        genres=[
            MovieGenre(name=genre['name'])
            for genre in film['genres']
            if genre is not None
        ],
    )


@backoff_public_methods()
class MovieApi:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.deserialize = deserialize_movie_json

    @with_aiohttp_session
    async def get_single(self, session: ClientSession, movie_id: str) -> Optional[MovieApiResponse]:
        url = '{url}/{id}'.format(url=self.base_url, id=movie_id)
        async with session.get(url) as response:
            if response.status == HTTPStatus.OK:
                movie = await response.json()
                return self.deserialize(movie)
            return None

    @with_aiohttp_session
    async def get_several(self, session: ClientSession, movie_ids: List[str]) -> List[Optional[MovieApiResponse]]:
        """Fetch details for multiple movies by their IDs."""
        param_tokens = ['id={id}'.format(id=movie_id) for movie_id in movie_ids]
        ids_param = '&'.join(param_tokens)
        url = '{url}/?{ids}'.format(url=self.base_url, ids=ids_param)
        async with session.get(url) as response:
            if response.status == HTTPStatus.OK:
                movies = await response.json()
                return [self.deserialize(movie) for movie in movies]
            return []
