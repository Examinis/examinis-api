from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from examinis.common.schemas.pagination_schema import PageParams
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


class ExamCreationSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    title: str = Field(str, min_length=1, max_length=100)
    instructions: Optional[str] = Field(None, max_length=512)
    subject_id: int


class ExamManualCreationSchema(ExamCreationSchema, ExamValidationMixin):
    questions: List[int]


class ExamAutomaticCreationSchema(ExamCreationSchema):
    amount: int = Field(5, ge=5, le=20)


class ExamListSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True
    )

    id: int
    title: str
    instructions: Optional[str] = None
    user: UserSchema
    subject: SubjectSchema
    created_at: datetime
    total_question: int

    @field_serializer('created_at')
    def serialize_created_at(self, created_at: datetime) -> str:
        return created_at.strftime('%d/%m/%Y %H:%M:%S')


class ExamPageParams(PageParams):
    subject_id: Optional[int] = None
    user_id: Optional[int] = None
