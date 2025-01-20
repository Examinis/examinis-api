from typing import List

from pydantic import BaseModel, ConfigDict, Field

from examinis.modules.difficulty.schemas import DifficultySchema
from examinis.modules.option.schemas import OptionCreateSchema, OptionSchema
from examinis.modules.subject.schemas import SubjectSchema


class QuestionBaseSchema(BaseModel):
    text: str
    subject_id: int
    difficulty_id: int


class QuestionSchema(QuestionBaseSchema):
    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True
    )

    id: int
    subject: SubjectSchema
    difficulty: DifficultySchema
    options: List[OptionSchema] = Field(default_factory=list)


class QuestionCreateSchema(QuestionBaseSchema):
    options: List[OptionCreateSchema]


class QuestionUpdateSchema(QuestionBaseSchema):
    pass
