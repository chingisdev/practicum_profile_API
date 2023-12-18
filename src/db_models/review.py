from typing import Dict, List, Type

from motor.core import AgnosticDatabase
from pydantic import BaseModel

from src.db_models.mongo_base_model import MongoBaseModel


class ReviewDocument(BaseModel):
    id: str
    user_id: str
    movie_id: str
    review: str

    @classmethod
    def from_mongo(cls: Type['ReviewDocument'], doc: Dict) -> 'ReviewDocument':
        doc['id'] = str(doc['_id'])
        return cls(**doc)


class ReviewModel(MongoBaseModel[ReviewDocument]):
    def __init__(self, database: AgnosticDatabase):
        super().__init__(database, 'reviews', ReviewDocument.from_mongo)

    async def add_review(self, user_id: str, movie_id: str, review: str) -> ReviewDocument:
        insert_dict = {'user_id': user_id, 'movie_id': movie_id, 'review': review}
        inserted = await self.collection.insert_one(insert_dict)
        return ReviewDocument(id=inserted.inserted_id, user_id=user_id, movie_id=movie_id, review=review)

    async def remove_review(self, review_id: str) -> None:
        await self.collection.delete_one({'_id': review_id})  # Assuming there's an 'id' field

    async def get_reviews_by_movie(self, movie_id: str) -> List[ReviewDocument]:
        return await self.find({'movie_id': movie_id})

    async def update_review(self, review_id: str, user_id: str, new_review_content: str) -> bool:
        update_result = await self.collection.update_one(
            {'_id': review_id},
            {'$set': {'review': new_review_content}},
        )

        return update_result.modified_count != 0
