import select
from typing import Optional

from fastapi import Depends
from sqlalchemy import select

from examinis.core.repository_abstract import RepositoryAbstract, Session
from examinis.db.config import get_session
from examinis.models.user import User


class AuthRepository(RepositoryAbstract[User]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(User, session=session)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.execute(stmt).scalars().first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        return self.session.execute(stmt).scalars().first()
