from typing import List

from pydantic import BaseModel, ConfigDict

from examinis.modules.question.schemas import QuestionExamSchema
from examinis.modules.user.schemas import UserSchema


class ExamSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    instructions: str
    created_at: str
    creator: UserSchema
    questions: List[QuestionExamSchema]


class ExamCreateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str


class ExamUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str
