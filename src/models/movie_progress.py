from pydantic import BaseModel


class MovieProgress(BaseModel):
    id: str
    title: str
    seconds_length: int
    current_progress: int
