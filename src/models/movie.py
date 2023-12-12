from typing import Optional

from pydantic import BaseModel, Field


class WatchProgress(BaseModel):
    progress: float = Field(default=0)


class MovieSummaryAggregation(BaseModel):
    movie_id: str
    likes_count: int
    user_liked: bool
    watch_progress: WatchProgress


class MovieDetailedAggregation(BaseModel):
    movie_id: str
    likes_count: int
    user_liked: bool
    bookmarks_count: int
    user_bookmarked: bool
    watch_progress: WatchProgress


class MoviePerson(BaseModel):
    """
    Represents a person associated with a film.

    Attributes:
    - id (Str): Unique identifier.
    - full_name (str): The name of the person.
    """

    id: str
    full_name: str


class MoviePersonName(BaseModel):
    """
    Represents a short version of person associated with a film.

    Attributes:
    - full_name (str): The full_name of the person.
    """

    full_name: str


class MovieGenre(BaseModel):
    """
    Represents a genre associated with a film

    Attributes:
        - name (str): The name of genre
    """

    name: str


class MovieApiResponse(BaseModel):
    """
    Represents a film.

    Attributes:
    - id (UUID): Unique identifier
    - title (str): The title of the film.
    - description (Optional[str]): The description of the film (if available).
    - imdb_rating (Optional[str]): The rating of the film (if available).
    - actors (Optional[List[Person]]): List of actors associated with the film (if available).
    - writers (Optional[List[Person]]): List of writers associated with the film (if available).
    - directors (Optional[List[Person]]): List of directors associated with the film (if available).
    - genres (Optional[List[Genre]]): List of genres associated with the film (if available).
    """

    id: str
    title: str
    description: str | None
    imdb_rating: float | None
    actors: list[MoviePerson] | None
    writers: list[MoviePerson] | None
    directors: list[MoviePersonName] | None
    genres: list[MovieGenre] | None


class MovieDetailedResponse(BaseModel):
    movie: MovieApiResponse
    movie_ugc_details: Optional[MovieDetailedAggregation]


class MovieSummaryResponse(BaseModel):
    movie: MovieApiResponse
    movie_ugc_details: Optional[MovieSummaryAggregation]
