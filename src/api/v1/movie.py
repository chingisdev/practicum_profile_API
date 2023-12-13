from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from models.movie import MovieDetailedResponse, MovieSummaryResponse
from models.user import User
from src.auxiliary_services.movie_search import MovieSearch
from src.dependencies.auth import get_user_from_request_state
from src.endpoint_services.bookmark import get_bookmark_service
from src.endpoint_services.like import get_like_service
from src.endpoint_services.watch_progress import get_watch_progress_service

router = APIRouter()


@router.get(
    '/bookmarks',
    summary="Get user's bookmarks",
)
async def get_user_bookmarked_movies(
    page_size: Annotated[int, Query(description='Items on page', ge=1)] = 50,
    page_number: Annotated[int, Query(description='Page number', ge=0)] = 0,
    user: User = Depends(get_user_from_request_state),
    search: MovieSearch = Depends(get_bookmark_service),
) -> Optional[List[MovieSummaryResponse]]:
    try:
        return await search.get_user_movies(user_id=user.id, page_number=page_number, page_limit=page_size)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong.')


@router.get(
    '/likes',
    summary='Get user liked movies',
)
async def get_user_liked_movies(
    page_size: Annotated[int, Query(description='Items on page', ge=1)] = 50,
    page_number: Annotated[int, Query(description='Page number', ge=0)] = 0,
    user: User = Depends(get_user_from_request_state),
    search: MovieSearch = Depends(get_like_service),
) -> Optional[List[MovieSummaryResponse]]:
    try:
        return await search.get_user_movies(user_id=user.id, page_number=page_number, page_limit=page_size)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong.')


@router.get(
    '/history',
    summary='Get user watched movies',
)
async def get_user_watched_movies(
    page_size: Annotated[int, Query(description='Items on page', ge=1)] = 50,
    page_number: Annotated[int, Query(description='Page number', ge=0)] = 0,
    user: User = Depends(get_user_from_request_state),
    search: MovieSearch = Depends(get_watch_progress_service),
) -> Optional[List[MovieSummaryResponse]]:
    try:
        return await search.get_user_movies(user_id=user.id, page_number=page_number, page_limit=page_size)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong.')


@router.get(
    '/movie/{movie_id}',
    summary="Get detailed info about movie. Included: general ugc, user's ugc",
)
async def get_movie_info(
    movie_id: str,
    user: User = Depends(get_user_from_request_state),
    search: MovieSearch = Depends(get_watch_progress_service),
) -> MovieDetailedResponse:
    try:
        return await search.get_movie(user_id=user.id, movie_id=movie_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Something went wrong.')
