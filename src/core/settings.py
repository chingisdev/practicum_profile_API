import json
import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

is_docker = os.environ.get('IS_DOCKER', False)

env_path = (
    '.env'
    if is_docker
    else str(Path(__file__).parents[3] / '.ugc.env.development')
)


KAFKA_PORT_DEV = 9093
MONGO_PORT_DEV = 27017
AUTH_PORT_DEV = 8000


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, extra='ignore')

    project_name: str = Field(default='user_profile')

    api_path: str = Field(default='/api/v1')

    kafka_host: str = Field(default='127.0.0.1', examples=['localhost', 'kafka'])
    kafka_port: int = Field(default=KAFKA_PORT_DEV)
    view_progress_topic: str = Field(default='view_progress')
    ugc_topic: str = Field(default='ugc')

    mongo_host: str = Field(default='127.0.0.1', examples=['localhost', 'mongodb'])
    mongo_port: int = Field(default=MONGO_PORT_DEV)
    mongo_database: str = Field(default='moviesUGC')

    token_bucket_capacity: int = Field(default=10)
    token_bucket_rate: int = Field(default=1)

    auth_host: str = Field(default='localhost')
    auth_port: int = Field(default=AUTH_PORT_DEV)
    auth_user_endpoint: str = Field(default='/api/v1/users/me')
    auth_enabled: bool = Field(default=False)
    production_mode: bool = Field(default=False)

    @property
    def auth_service_url(self) -> str:
        return 'http://{host}:{port}{endpoint}'.format(
            host=self.auth_host, port=self.auth_port, endpoint=self.auth_user_endpoint,
        )

    @property
    def mongo_database_url(self) -> str:
        return 'mongodb://{host}:{port}'.format(host=self.mongo_host, port=self.mongo_port)

    @property
    def kafka_bootstrap_servers(self) -> str:
        return '{host}:{port}'.format(host=self.kafka_host, port=self.kafka_port)

    @property
    def kafka_config(self) -> dict:
        return {
            'bootstrap_servers': self.kafka_bootstrap_servers,
            'key_serializer': str.encode,
            'value_serializer': lambda topic_value: json.dumps(topic_value).encode('utf-8'),
            'linger_ms': 10,
            'acks': 0,
        }

    @property
    def kafka_topics(self) -> tuple:
        return self.view_progress_topic, self.ugc_topic


settings = Settings()