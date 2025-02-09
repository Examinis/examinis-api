from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from examinis.core.RepositoryAbstract import RepositoryAbstract
from examinis.db.config import get_session
from examinis.models import Question


class QuestionRepository(RepositoryAbstract[Question]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(Question, session=session)

    def get_by_list(self, question_ids: List[int]) -> List[Question]:
        return (
            self.session.query(Question)
            .filter(Question.id.in_(question_ids))
            .all()
        )
