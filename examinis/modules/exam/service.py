from http import HTTPStatus

from fastapi import Depends, HTTPException

from examinis.common.schemas.pagination_schema import PageParams, PagedResponseSchema
from examinis.core.ServiceAbstract import ServiceAbstract
from examinis.models.exam import Exam
from examinis.modules.exam.repository import ExamRepository
from examinis.modules.exam.schemas import (
    ExamAutomaticCreationSchema,
    ExamListSchema,
    ExamManualCreationSchema,
    ExamPageParams,
)
from examinis.modules.question.service import QuestionService


class ExamService(ServiceAbstract[Exam]):
    def __init__(
        self,
        repository: ExamRepository = Depends(ExamRepository),
        question_service: QuestionService = Depends(QuestionService),
    ):
        super().__init__(repository)
        self.repository = repository
        self.question_service = question_service

    def get(self, id: int) -> Exam:
        exam = self.repository.get(id)

        if not exam:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Exam not found',
            )

        return exam

    def get_all_paginated(self, params: ExamPageParams) -> PagedResponseSchema[ExamListSchema]:
        items = self.repository.get_all_paginated(params)
        total = self.repository.count_all()

        transformed_items = [
        {
            'id': exam.id,
            'title': exam.title,
            'user': {
                'id': exam.user.id,
                'name': exam.user.name,
            },
            'subject': {
                'id': exam.subject.id,
                'name': exam.subject.name,
            },
            'created_at': exam.created_at,
            'total_question': len(exam.questions),
        }
        for exam in items
    ]

        return PagedResponseSchema[ExamListSchema](
            total=total,
            page=params.page,
            size=params.size,
            results=items,)

    def create_manual(self, exam: ExamManualCreationSchema) -> Exam:
        questions = self.question_service.get_by_list(exam.questions)

        if len(questions) != len(exam.questions):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Invalid question ids',
            )

        exam_in = exam.model_dump(exclude={'questions'})
        exam_in['user_id'] = 2   # Professor id at the moment

        return self.repository.create_manual(exam_in, questions)

    def create_automatic(self, exam: ExamAutomaticCreationSchema) -> Exam:
        questions = self.question_service.get_random_by_subject(
            exam.subject_id,
            exam.amount,
        )

        exam_in = exam.model_dump(exclude={'amount'})
        exam_in['user_id'] = 2   # Professor id at the moment

        return self.repository.create_manual(exam_in, questions)
