import asyncio
import logging
from pprint import pformat

from tests.debugging.http_client import make_request

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def run_basic_user_scenario():
    # 1. Регистрируем пользователя в сервисе Auth:
    sign_up_url = 'http://localhost:80/auth/api/v1/auth/signup'

    user_email = 'deedeeking@ramones123.com'
    user_pass = '53rdAnd3rd123'

    new_user_data = {
        'first_name': 'DeeDee123',
        'last_name': 'Ramone123',
        'disabled': False,
        'email': user_email,
        'password': user_pass,
    }

    auth_response = await make_request(  # noqa: WPS430 здесь необходимо использовать вложенную функцию
        method='POST',
        endpoint_url=sign_up_url,
        body=new_user_data,
    )

    logger.info(pformat(auth_response))


    # 2. Логиним пользователя в сервисе Auth:
    login_url = 'http://localhost:80/auth/api/v1/auth/login'
    login_form_data = {
        'username': user_email,
        'password': user_pass,
    }

    login_response = await make_request(  # noqa: WPS430 здесь необходимо использовать вложенную функцию
        method='POST',
        endpoint_url=login_url,
        form_data=login_form_data,
    )

    logger.info(pformat(login_response))
    # Получаем access и refresh токены;
    # 3. Проверяем свои данные в Auth:

    access_token = login_response.body['access_token']

    header = {'Authorization': 'Bearer {access_token}'.format(access_token=access_token)}

    me_url = 'http://localhost:80/auth/api/v1/users/me'

    me_response = await make_request(method='GET', endpoint_url=me_url, header=header)

    logger.info(pformat(me_response))

    # 3. Обращаемся в эндпойнт пользовательского профиля Profile API,
    # чтобы отредактировать информацию о себе.

    # PATCH localhost:8000/profile/api/v1/profile

    profile_url = 'http://localhost:8000/api/v1/profile/'

    profile_data = {
        'first_name': 'DD',
        'last_name': 'King',
        'phone': '911',
    }

    profile_response = await make_request(
        method='PATCH',
        endpoint_url=profile_url,
        header=header,
        body=profile_data,
    )

    logger.info(pformat(profile_response))

if __name__ == '__main__':
    asyncio.run(run_basic_user_scenario())
