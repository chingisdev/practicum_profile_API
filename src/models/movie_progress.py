from pydantic import BaseModel


class MovieProgress(BaseModel):
    id: str
    break_point: int
