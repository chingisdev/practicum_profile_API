from typing import Dict, List, Optional

from models.movie import MovieApiResponse, MovieDetailedResponse, MovieSummaryAggregation, MovieSummaryResponse
from src.auxiliary_services.cache_service import CacheService
from src.auxiliary_services.data_aggregation import AbstractSummaryAggregator, MovieDetailedAggregator
from src.external_api.movie import MovieApi, deserialize_movie_json


def get_empty(pairs: dict) -> List[str]:
    empty_keys = []
    for key, movie in pairs.items():
        if movie is None:
            empty_keys.append(key)
    return empty_keys


def build_movie_response(
    movie_details: List[MovieSummaryAggregation],
    cached_movies: Dict[str, MovieApiResponse],
) -> List[MovieSummaryResponse]:
    movies = []
    for movie_detail in movie_details:
        movie_from_api = cached_movies[movie_detail.movie_id]
        movie_response = MovieSummaryResponse(movie=movie_from_api, movie_ugc_details=movie_detail)
        movies.append(movie_response)
    return movies


class MovieSearch:
    def __init__(
        self,
        cache: CacheService,
        detailed_aggregator: MovieDetailedAggregator,
        summary_aggregator: AbstractSummaryAggregator,
        movie_api: MovieApi,
    ):
        self._cache = cache
        self._summary_aggregator = summary_aggregator
        self._detailed_aggregator = detailed_aggregator
        self._movie_api = movie_api
        self._movie_deserializer = deserialize_movie_json

    async def get_user_movies(
        self,
        user_id: str,
        page_number: int = 0,
        page_limit: int = 0,
    ) -> Optional[List[MovieSummaryResponse]]:

        movie_summaries = await self._summary_aggregator.aggregate(
            user_id=user_id, page_number=page_number, page_limit=page_limit,
        )
        if not movie_summaries:
            return None
        movie_ids = [summary.movie_id for summary in movie_summaries]
        movies = await self._get_movies(movie_ids=movie_ids)
        return build_movie_response(movie_details=movie_summaries, cached_movies=movies)

    async def get_movie(self, user_id: str, movie_id: str) -> MovieDetailedResponse:
        movie_info = await self._detailed_aggregator.aggregate(user_id=user_id, movie_id=movie_id)
        movie = await self._get_movie(movie_id=movie_id)
        return MovieDetailedResponse(movie=movie, movie_ugc_details=movie_info)

    async def _get_movie(self, movie_id: str) -> MovieApiResponse:
        movie_from_cache = await self._cache.get_single(key=movie_id)
        if movie_from_cache is None:
            movie_from_api = await self._movie_api.get_single(movie_id=movie_id)
            await self._cache.store_single(key=movie_id, to_store=movie_from_api.model_dump())
            return movie_from_api
        return self._movie_deserializer(movie_from_cache)

    async def _fetch_missing_movies(self, missing_ids: List[str]) -> Dict[str, MovieApiResponse]:
        films = await self._movie_api.get_several(keys=missing_ids)
        to_store = {film.id: film.model_dump() for film in films}
        await self._cache.store_many(to_store=to_store)
        return to_store

    async def _get_movies(self, movie_ids: List[str]) -> Dict[str, MovieApiResponse]:
        movies_from_cache = await self._cache.get_many(keys=movie_ids)
        missing_ids = get_empty(movies_from_cache)

        if missing_ids:
            fetched_movies = await self._fetch_missing_movies(missing_ids)
            movies_from_cache |= fetched_movies

        return {
            movie_id: self._movie_deserializer(movie_json)
            for movie_id, movie_json in movies_from_cache.items()
        }
