from fastapi import Depends

from examinis.core.repository_abstract import RepositoryAbstract, Session
from examinis.db.config import get_session
from examinis.models import UserStatus


class UserStatusRepository(RepositoryAbstract[UserStatus]):
    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(UserStatus, session=session)
