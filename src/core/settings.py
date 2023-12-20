import json
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

is_docker = os.environ.get('IS_DOCKER', False)

env_path = (
    '.env'
    if is_docker
    else str(Path(__file__).parents[3] / '.ugc.env.development')
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, extra='ignore')
    # 1.1. Profile API itself:
    project_name: str

    api_path: str

    token_bucket_capacity: int
    token_bucket_rate: int

    # 1.2. Profile API Redis:
    redis_host: str
    redis_port: int

    # 1.3. Profile API Kafka:
    kafka_host: str
    kafka_port: int
    watch_progress_topic: str
    ugc_topic: str

    # 1.4. Profile API Mongo:
    mongo_host: str
    mongo_port: int
    mongo_database: str

    # 2.1. Auth API:
    auth_host: str
    auth_port: int
    auth_user_endpoint: str
    auth_enabled: bool
    production_mode: bool

    # 3.1. Movies API
    movie_endpoint: str

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
        return self.watch_progress_topic, self.ugc_topic


settings = Settings()
