from fastapi import Depends
from sqlalchemy.orm import Session

from examinis.core.repository_abstract import RepositoryAbstract
from examinis.db.config import get_session
from examinis.models import Option


class OptionRepository(RepositoryAbstract[Option]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(Option, session=session)

    def delete_by_question_id(self, question_id: int) -> None:
        self.session.query(Option).filter_by(question_id=question_id).delete()
        self.session.commit()
