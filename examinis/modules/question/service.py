import os
from http import HTTPStatus
from typing import List
from uuid import uuid4

from fastapi import Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse

from examinis.common.validators.image_upload_validator import (
    ImageUploadValidation,
)
from examinis.core.ServiceAbstract import ServiceAbstract
from examinis.models.question import Question
from examinis.modules.option.service import OptionService
from examinis.modules.question.repository import QuestionRepository
from examinis.modules.question.schemas import (
    QuestionCreateSchema,
    QuestionUpdateSchema,
)


class QuestionService(ServiceAbstract[Question]):
    def __init__(
        self,
        repository: QuestionRepository = Depends(QuestionRepository),
        option_service: OptionService = Depends(OptionService),
    ):
        super().__init__(repository)
        self.option_service = option_service
        self.repository = repository

    def get(self, id: int) -> Question:
        question = self.repository.get(id)

        if not question:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Question not found'
            )

        return question

    def create(self, question: QuestionCreateSchema) -> Question:
        question_in = question.model_dump()
        question_in.pop('options')
        question_in['user_id'] = 1

        question_db = self.repository.create(question_in)
        options = self.option_service.create_by_list(
            question_db.id, question.options
        )

        question_db.options = options
        return question_db

    def delete(self, id: int) -> None:
        question = self.get(id)
        self.option_service.delete_by_question_id(question.id)

        if question.image_path:
            try:
                os.remove(question.image_path)
            except FileNotFoundError:
                pass

        self.repository.delete(id)

    def update(self, question: QuestionUpdateSchema) -> Question:
        question_db = self.get(question.id)

        question_in = question.model_dump()
        question_in.pop('options')

        question_db = self.repository.update(question_db.id, question_in)

        self.option_service.delete_by_question_id(question.id)

        options = self.option_service.create_by_list(
            question_db.id, question.options
        )

        question_db.options = options

        return question_db

    async def upload_image(self, question_id: int, image: UploadFile):
        ImageUploadValidation.validate_image(image)

        question = self.get(question_id)

        if question.image_path:
            try:
                os.remove(question.image_path)
            except FileNotFoundError:
                pass

        image_extension = image.filename.split('.')[-1]
        image.filename = f'{uuid4()}.{image_extension}'
        image_path = f'uploaded_images/{image.filename}'

        with open(image_path, 'wb') as buffer:
            buffer.write(await image.read())

        return self.repository.update(question_id, {'image_path': image_path})

    def get_image(self, question_id: int):
        question = self.get(question_id)

        if not question.image_path:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Image not found'
            )

        image_extension = question.image_path.split('.')[-1]

        return FileResponse(
            path=question.image_path, media_type=f'image/{image_extension}'
        )

    def get_by_list(self, ids: List[int]) -> List[Question]:
        return self.repository.get_by_list(ids)

    def get_random_by_subject(
        self, subject_id: int, amount: int
    ) -> List[Question]:
        return self.repository.get_random_by_subject(subject_id, amount)
