from typing import Optional

from services.external_api.movie import MovieApi

movie_api: Optional[MovieApi] = None


def get_movie_api() -> Optional[MovieApi]:
    return movie_api
