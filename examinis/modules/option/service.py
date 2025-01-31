from typing import List

from fastapi import Depends, HTTPException

from examinis.core.ServiceAbstract import ServiceAbstract
from examinis.models.option import Option
from examinis.modules.option.repository import OptionRepository
from examinis.modules.option.schemas import OptionCreateSchema


class OptionService(ServiceAbstract[Option]):
    def __init__(
        self, repository: OptionRepository = Depends(OptionRepository)
    ):
        super().__init__(repository)

    def get(self, id: int) -> Option:
        option = self.repository.get(id)

        if not option:
            raise HTTPException(status_code=404, detail='Option not found')

        return option

    def create_by_list(
        self, question_id: int, options: List[OptionCreateSchema]
    ) -> List[Option]:
        options_db = []

        for option in options:
            option_dict = option.dict()
            option_dict['question_id'] = question_id

            option_db = self.create(option_dict)
            options_db.append(option_db)

            if option.is_correct:
                self.repository.create_correct_option(
                    question_id, option_db.id
                )

        return options_db

    def delete_by_question_id(self, question_id: int) -> None:
        self.repository.delete_by_question_id(question_id)
