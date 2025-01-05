from pydantic import BaseModel


class OptionSchema(BaseModel):
    id: int
    description: str


class OptionCreateSchema(BaseModel):
    description: str
    letter: str
    is_correct: bool
