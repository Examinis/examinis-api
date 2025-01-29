from fastapi import Depends, HTTPException

from examinis.core.ServiceAbstract import ServiceAbstract
from examinis.models.difficulty import Difficulty
from examinis.modules.difficulty.repository import DifficultyRepository


class DifficultyService(ServiceAbstract[Difficulty]):
    def __init__(
        self, repository: DifficultyRepository = Depends(DifficultyRepository)
    ):
        super().__init__(repository)

    def get(self, id: int) -> Difficulty:
        difficulty = self.repository.get(id)

        if not difficulty:
            raise HTTPException(status_code=404, detail='Difficulty not found')

        return difficulty
