from fastapi import Depends, HTTPException

from examinis.core.ServiceAbstract import ServiceAbstract
from examinis.models.exam import Exam
from examinis.modules.exam.repository import ExamRepository


class ExamService(ServiceAbstract[Exam]):
    def __init__(self, repository: ExamRepository = Depends(ExamRepository)):
        super().__init__(repository)

    def get(self, id: int) -> Exam:
        exam = self.repository.get(id)

        if not exam:
            raise HTTPException(status_code=404, detail='Exam not found')

        return exam
