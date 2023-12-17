"""Тесты ресурса roles."""
import logging
from http import HTTPStatus

import pytest

from tests.functional.db.record import add_record
from tests.functional.db.user import prepare_authenticated_user
from tests.functional.models.movies.filmwork import Filmwork
from tests.functional.testdata import auth as auth_data
from tests.functional.testdata import movies as movies_data

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# Все тесты будут считаться помеченными следующей меткой:
pytestmark = pytest.mark.asyncio


# тест эндпойнта /movie/{movie_id}

async def test_movies_query(
    auth_api_pg_session,
    movies_api_pg_session,
    auth_api_redis_client,
    movies_api_redis_client,
    make_api_request,
):
    """Протестировать запрос о фильме по его id.

    Args:
        pg_session: фикстура, создающая экземпляр сессии клиента postgres
        make_api_request: фикстура, возвращающая метод http запроса
    """
    # 1. Добавляем фильм в бд Movies API:
    movie_in_db = await add_record(
        pg_session=movies_api_pg_session,
        model=Filmwork,
        filler=movies_data.filmworks.RNR_HIGHSCHOOL,
    )

    # 2. Готовим "вошедшего" пользователя:
    test_user = auth_data.users.JOEY

    access_token, refresh_token, user_id = await prepare_authenticated_user(
        pg_session=auth_api_pg_session,
        redis_client=auth_api_redis_client,
        new_user=test_user,
    )

    # 3. Делаем запрос в Profile API на эндпойнт /movies
    header = {'Authorization': 'Bearer {access_token}'.format(access_token=access_token)}

    # Предварительно узнаём id фильма, находящегося в б.д.:
    movie_id = movie_in_db.id

    response = await make_api_request(
        method='POST',
        resource='collection/movie/',
        pk=movie_id,
        header=header,
    )

    # проверяем статус код ответа:
    assert response.status == HTTPStatus.OK

    # проверяем количество фильмов в выдаче:
    assert len(response.body) == 1
