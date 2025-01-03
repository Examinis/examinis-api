from typing import Generic, Optional, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm.session import Session

from examinis.db.config import get_session
from examinis.models import Base

T = TypeVar('T', bound=Base)


class RepositoryAbstract(Generic[T]):
    def __init__(self, model: Type[T], session: Session = Depends(get_session)):
        self.model = model
        self.session = session

    def create(self, obj_in: dict) -> T:
        instance = self.model(**obj_in)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)

    def get_all(self) -> list[T]:
        return self.session.query(self.model).all()
