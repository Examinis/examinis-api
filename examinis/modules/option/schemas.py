from typing import Optional

from pydantic import BaseModel


class OptionSchema(BaseModel):
    id: int
    description: str
    letter: str
    is_correct: bool


class OptionCreateSchema(BaseModel):
    description: str
    letter: str
    is_correct: bool


class OptionUpdateSchema(BaseModel):
    id: Optional[int] = None
    description: str
    letter: str
    is_correct: bool
