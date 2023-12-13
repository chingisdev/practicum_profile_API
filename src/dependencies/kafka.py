from typing import TypeAlias

from aiokafka import AIOKafkaProducer  # type: ignore

AsyncKafkaProducer: TypeAlias = AIOKafkaProducer

kafka_producer: AsyncKafkaProducer | None = None


def get_kafka_producer() -> AsyncKafkaProducer:
    return kafka_producer
