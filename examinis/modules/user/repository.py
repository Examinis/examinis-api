from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from examinis.core.repository_abstract import RepositoryAbstract
from examinis.db.config import get_session
from examinis.models import User


class UserRepository(RepositoryAbstract[User]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(User, session=session)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()
