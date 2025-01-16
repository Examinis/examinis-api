from typing import List

from pydantic import BaseModel, ConfigDict, Field

from examinis.modules.difficulty.schemas import DifficultySchema
from examinis.modules.option.schemas import OptionCreateSchema, OptionSchema
from examinis.modules.subject.schemas import SubjectSchema


class QuestionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int
    text: str
    subject: SubjectSchema
    difficulty: DifficultySchema
    options: List[OptionSchema] = Field(default_factory=list)


class QuestionCreateSchema(BaseModel):
    text: str
    subject_id: int
    difficulty_id: int
    options: List[OptionCreateSchema]
