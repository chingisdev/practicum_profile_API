from abc import ABC, abstractmethod

from aiokafka import AIOKafkaProducer  # type: ignore


class AsyncMessageBroker(ABC):
    @abstractmethod
    async def send(self, key: str, message: dict) -> None:
        raise NotImplementedError


class KafkaAsyncMessageBroker(AsyncMessageBroker):
    def __init__(self, producer: AIOKafkaProducer, topic: str):
        self.producer = producer
        self.topic = topic

    async def send(self, key: str, message: dict) -> None:
        await self.producer.send(topic=self.topic, key=key, value=message)
