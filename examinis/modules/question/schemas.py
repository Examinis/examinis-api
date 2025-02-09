import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from examinis.modules.difficulty.schemas import DifficultySchema
from examinis.modules.option.schemas import OptionInSchema, OptionSchema
from examinis.modules.option.validators import OptionsValidationMixin
from examinis.modules.subject.schemas import SubjectSchema
from examinis.modules.user.schemas import UserSchema


class QuestionBaseSchema(BaseModel):
    text: str
    subject_id: int
    difficulty_id: int


class QuestionSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    id: int
    text: str
    created_at: datetime

    user: UserSchema
    subject: SubjectSchema
    difficulty: DifficultySchema
    options: List[OptionSchema] = Field(default_factory=list)


class QuestionCreateSchema(QuestionBaseSchema, OptionsValidationMixin):
    options: List[OptionInSchema]


class QuestionUpdateSchema(QuestionBaseSchema, OptionsValidationMixin):
    id: int
    options: List[OptionInSchema]


class QuestionExamSchema(BaseModel):
    id: int
    text: str
    options: List[OptionSchema]
