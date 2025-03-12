from fastapi import Depends
from sqlalchemy.orm import Session

from examinis.core.repository_abstract import RepositoryAbstract
from examinis.db.config import get_session
from examinis.models import Subject


class SubjectRepository(RepositoryAbstract[Subject]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(Subject, session=session)
