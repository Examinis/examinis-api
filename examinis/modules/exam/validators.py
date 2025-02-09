from typing import List

from pydantic import field_validator

from examinis.modules.question.schemas import QuestionExamSchema

MIN_QUESTION = 5
MAX_QUESTION = 20


class ExamValidationMixin:
    @field_validator('questions')
    @classmethod
    def validate_questions(
        cls, questions: List[QuestionExamSchema]
    ) -> List[QuestionExamSchema]:
        if not (MIN_QUESTION <= len(questions) <= MAX_QUESTION):
            raise ValueError(
                f'A Exam must have between {MIN_QUESTION} and {MAX_QUESTION} questions.'
            )
        return questions
