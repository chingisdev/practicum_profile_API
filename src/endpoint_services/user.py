from functools import lru_cache

from fastapi import Depends

from core.settings import settings
from src.db_models.user import UserModel
from src.dependencies.mongo import AsyncMongoClient, get_mongo_client


@lru_cache()
def get_user_model(
    client: AsyncMongoClient = Depends(get_mongo_client),
) -> UserModel:
    db = client[settings.mongo_database]
    return UserModel(db)
