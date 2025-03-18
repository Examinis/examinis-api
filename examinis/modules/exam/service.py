from datetime import datetime
from http import HTTPStatus
from typing import Dict, List

from fastapi import Depends, HTTPException

from examinis.common.schemas.pagination_schema import PagedResponseSchema
from examinis.core.service_abstract import ServiceAbstract
from examinis.models.exam import Exam
from examinis.models.option import Option
from examinis.models.question import Question
from examinis.modules.exam.repository import ExamRepository
from examinis.modules.exam.schemas import (
    ExamAutomaticCreationSchema,
    ExamCorrectionSchema,
    ExamListSchema,
    ExamManualCreationSchema,
    ExamPageParams,
)
from examinis.modules.option.schemas import OptionCorrectedSchema
from examinis.modules.question.schemas import QuestionCorrectSchema
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

    def get_all_paginated(
        self, params: ExamPageParams
    ) -> PagedResponseSchema[ExamListSchema]:
        items = self.repository.get_all_paginated(params)
        total = self.repository.count_filtered(params)

        results = [ExamListSchema.from_orm(item) for item in items]

        return PagedResponseSchema[ExamListSchema](
            total=total,
            page=params.page,
            size=params.size,
            results=results,
        )

    def create_manual(
        self, exam: ExamManualCreationSchema, user_id: int
    ) -> Exam:
        questions = self.question_service.get_by_list(exam.questions)

        if len(questions) != len(exam.questions):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Invalid question ids',
            )

        exam_in = exam.model_dump(exclude={'questions'})
        exam_in['user_id'] = user_id

        return self.repository.create_manual(exam_in, questions)

    def create_automatic(
        self, exam: ExamAutomaticCreationSchema, user_id: int
    ) -> Exam:
        questions = self.question_service.get_random_by_subject(
            exam.subject_id,
            exam.amount,
        )

        if len(questions) != exam.amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Not enough questions for the selected subject',
            )

        exam_in = exam.model_dump(exclude={'amount'})
        exam_in['user_id'] = user_id

        return self.repository.create_manual(exam_in, questions)

    def grade(self, exam_id: int, answers: Dict) -> Dict:
        exam = self.get(exam_id)

        questions: List[Question] = exam.questions

        corrected_questions = []
        correct_questions = 0

        answers_dict = {
            str(a['question_id']): a['selected_option']
            for a in answers['answers']
        }

        for question in questions:
            options: List[Option] = question.options

            mapped_correct_options = {
                option.id: option.is_correct for option in options
            }

            answer = answers_dict.get(str(question.id))

            if answer is None:
                continue

            if mapped_correct_options.get(answer, False):
                correct_questions += 1

            question_model = QuestionCorrectSchema(
                id=question.id,
                text=question.text,
                options=[
                    OptionCorrectedSchema(
                        id=option.id,
                        description=option.description,
                        is_correct=option.is_correct,
                        selected=option.id == answer,
                        letter=option.letter,
                    )
                    for option in options
                ],
            )

            corrected_questions.append(question_model)

        score = (correct_questions / len(questions)) * 100 if questions else 0

        return ExamCorrectionSchema(
            id=exam.id,
            title=exam.title,
            instructions=exam.instructions,
            created_at=exam.created_at,
            answered_at=datetime.now(),
            user=exam.user,
            subject=exam.subject,
            questions=corrected_questions,
            score=score,
        )
