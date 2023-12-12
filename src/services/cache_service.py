from typing import Any, Dict, List, Optional, Protocol

from redis.asyncio import Redis

from utils.backoff import backoff_public_methods


class SerializerProtocol(Protocol):
    def dumps(self, to_convert: Any) -> Any:
        raise NotImplementedError

    def loads(self, to_convert: Any) -> Any:
        raise NotImplementedError


@backoff_public_methods()
class CacheService:
    def __init__(self, redis_client: Redis, serializer: SerializerProtocol, ttl: int = 300):
        self.redis_client = redis_client
        self.serializer = serializer
        self.ttl = ttl

    async def store_single(self, key: str, to_store: Any, ttl: Optional[int] = None) -> None:
        expiration_shift = ttl or self.ttl
        serialized_value = self.serializer.dumps(to_store)
        await self.redis_client.set(key, serialized_value, ex=expiration_shift)

    async def store_many(self, to_store: Dict[str, Any], ttl: Optional[int] = None) -> None:
        expiration_shift = ttl or self.ttl
        async with self.redis_client.pipeline() as pipe:
            for key, storable in to_store.items():
                serialized_value = self.serializer.dumps(storable)
                await pipe.set(key, serialized_value, ex=expiration_shift)
            await pipe.execute()

    async def get_single(self, key: str) -> Optional[Any]:
        extractable = await self.redis_client.get(key)
        if extractable:
            await self.redis_client.expire(key, self.ttl)
            return self.serializer.loads(extractable)
        return None

    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        async with self.redis_client.pipeline() as pipe:
            for key_element in keys:
                await pipe.get(key_element)
            to_extract = await pipe.execute()

        key_extractable_dictionary = {}
        for key, extractable in zip(keys, to_extract):
            if extractable:
                await self.redis_client.expire(key, self.ttl)
                key_extractable_dictionary[key] = self.serializer.loads(extractable)

        return key_extractable_dictionary
