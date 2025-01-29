from fastapi import Depends
from sqlalchemy.orm import Session

from examinis.core.RepositoryAbstract import RepositoryAbstract
from examinis.db.config import get_session
from examinis.models import Difficulty


class DifficultyRepository(RepositoryAbstract[Difficulty]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(Difficulty, session=session)
