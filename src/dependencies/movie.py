from typing import Optional

from src.external_api.movie import MovieApi

movie_api: Optional[MovieApi] = None


def get_movie_api() -> Optional[MovieApi]:
    return movie_api
