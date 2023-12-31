from typing import Dict, Optional, Type

from bson import ObjectId
from motor.core import AgnosticDatabase
from pydantic import BaseModel, EmailStr, Field

from src.db_models.mongo_base_model import MongoBaseModel
from src.models.user import UserUpdate


class UserDocument(BaseModel):
    id: Optional[str] = Field(alias='_id')
    username: str
    email: EmailStr
    full_name: Optional[str] = None

    @classmethod
    def from_mongo(cls: Type['UserDocument'], doc: Dict) -> 'UserDocument':
        doc['id'] = str(doc['_id'])
        return cls(**doc)


class UserModel(MongoBaseModel[UserDocument]):
    def __init__(self, database: AgnosticDatabase):
        super().__init__(database, 'users', UserDocument.from_mongo)

    async def create_user(self, user_document: UserDocument) -> None:
        user_dict = user_document.model_dump(by_alias=True, exclude={'id'}, exclude_none=True)
        await self.collection.insert_one(user_dict)

    async def update_user(self, user_id: str, update_data: UserUpdate) -> None:
        await self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data.model_dump(exclude_unset=True)},
            upsert=True,
        )

    async def get_user(self, user_id: str) -> Optional[UserDocument]:
        return await self.find_one({'_id': ObjectId(user_id)})
