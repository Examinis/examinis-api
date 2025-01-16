from fastapi import Depends, HTTPException

from examinis.core.ServiceAbstract import ServiceAbstract
from examinis.models.subject import Subject
from examinis.modules.subject.repository import SubjectRepository


class SubjectService(ServiceAbstract[Subject]):
    def __init__(
        self, repository: SubjectRepository = Depends(SubjectRepository)
    ):
        super().__init__(repository)

    def get(self, id: int) -> Subject:
        subject = self.repository.get(id)

        if not subject:
            raise HTTPException(status_code=404, detail='Subject not found')

        return subject
