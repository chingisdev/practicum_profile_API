from pydantic import BaseModel


class ReviewContent(BaseModel):
    review: str


class DeleteReview(BaseModel):
    id: str
