from typing import Generic, List, Optional, TypeVar

from examinis.common.schemas.pagination_schema import (
    PagedResponseSchema,
    PageParams,
)
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

    def get_all(self) -> List[T]:
        return self.repository.get_all()

    def get_all_paginated(self, params: PageParams) -> PagedResponseSchema[T]:
        total_items = self.repository.count_all()
        items = self.repository.get_all_paginated(params)

        return PagedResponseSchema[T](
            total=total_items,
            page=params.page,
            size=params.size,
            results=items
        )
