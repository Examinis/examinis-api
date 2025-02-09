from fastapi import Depends

from examinis.core.RepositoryAbstract import RepositoryAbstract, Session
from examinis.db.config import get_session
from examinis.models import Exam


class ExamRepository(RepositoryAbstract[Exam]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(Exam, session=session)
