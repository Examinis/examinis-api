from fastapi import Depends, HTTPException

from examinis.core.ServiceAbstract import ServiceAbstract
from examinis.models.question import Question
from examinis.modules.option.service import OptionService
from examinis.modules.question.repository import QuestionRepository
from examinis.modules.question.schemas import QuestionCreateSchema


class QuestionService(ServiceAbstract[Question]):
    def __init__(
        self,
        repository: QuestionRepository = Depends(QuestionRepository),
        option_service: OptionService = Depends(OptionService),
    ):
        super().__init__(repository)
        self.option_service = option_service

    def get(self, id: int) -> Question:
        question = self.repository.get(id)

        if not question:
            raise HTTPException(status_code=404, detail='Question not found')

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
        self.repository.delete(id)