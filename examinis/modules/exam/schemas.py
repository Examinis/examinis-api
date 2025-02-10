from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from examinis.modules.exam.validators import ExamValidationMixin
from examinis.modules.question.schemas import QuestionExamSchema
from examinis.modules.subject.schemas import SubjectSchema
from examinis.modules.user.schemas import UserSchema


class ExamSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

    id: int
    title: str
    instructions: Optional[str]
    created_at: datetime
    user: UserSchema
    subject: SubjectSchema
    questions: List[QuestionExamSchema]


class ExamManualCreationSchema(BaseModel, ExamValidationMixin):
    model_config = ConfigDict(extra='forbid')

    title: str = Field(str, min_length=1, max_length=100)
    instructions: Optional[str] = Field(None, max_length=512)
    subject_id: int
    questions: List[QuestionExamSchema]


class ExamAutomaticCreationSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    title: str = Field(str, min_length=1, max_length=100)
    instructions: Optional[str] = Field(None, max_length=512)
    subject_id: int
    amount: int = Field(5, ge=5, le=20)


class ExamUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str
