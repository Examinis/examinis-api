from typing import Optional

from pydantic import BaseModel


class OptionSchema(BaseModel):
    id: int
    description: str
    letter: str
    is_correct: bool


class OptionInSchema(BaseModel):
    description: str
    letter: str
    is_correct: bool
