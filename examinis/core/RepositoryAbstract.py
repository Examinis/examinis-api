from typing import Generic, List, Optional, Type, TypeVar

from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm.session import Session

from examinis.common.schemas.pagination_schema import PageParams
from examinis.db.config import get_session
from examinis.models import Base

T = TypeVar('T', bound=Base)


class RepositoryAbstract(Generic[T]):
    def __init__(
        self, model: Type[T], session: Session = Depends(get_session)
    ):
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

    def get_all(self) -> List[T]:
        return self.session.query(self.model).all()

    def get_all_paginated(self, params: PageParams) -> List[T]:
        query = self.session.query(self.model)
        if params.order_by:
            column = getattr(self.model, params.order_by, None)
            if column:
                if params.order_desc:
                    query = query.order_by(desc(column))
                else:
                    query = query.order_by(column)

        return (
            query.limit(params.size)
            .offset((params.page - 1) * params.size)
            .all()
        )

    def count_all(self) -> int:
        return self.session.query(self.model).count()

    def update(self, id: int, obj_in: dict) -> Optional[T]:
        instance = self.get(id)
        if instance:
            for key, value in obj_in.items():
                setattr(instance, key, value)
            self.session.commit()
            self.session.refresh(instance)
        return instance

    def delete(self, id: int) -> None:
        instance = self.get(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()