from fastapi import Depends
from sqlalchemy.orm import Session

from examinis.core.RepositoryAbstract import RepositoryAbstract
from examinis.db.config import get_session
from examinis.models import CorrectOption, Option


class OptionRepository(RepositoryAbstract[Option]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(Option, session=session)

    def create_correct_option(self, question_id: int, option_id: int) -> None:
        correct_option = CorrectOption(
            question_id=question_id, option_id=option_id
        )

        self.session.add(correct_option)
        self.session.commit()
