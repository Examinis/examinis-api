from typing import Generic, Optional, TypeVar

from examinis.core.RepositoryAbstract import RepositoryAbstract
from examinis.models import Base

T = TypeVar('T', bound=Base)


class ServiceAbstract(Generic[T]):
    def __init__(self, repository: RepositoryAbstract[T]):
        self.repository = repository

    def create(self, obj_in: dict) -> T:
        return self.repository.create(obj_in)

    def get(self, id: int) -> Optional[T]:
        return self.repository.get(id)

    def get_all(self) -> list[T]:
        return self.repository.get_all()
