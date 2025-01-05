from pydantic import BaseModel


class DifficultySchema(BaseModel):
    id: int
    name: str
