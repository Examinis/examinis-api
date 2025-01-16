from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from examinis.models import Base


class Difficulty(Base):
    __tablename__ = 'difficulty'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    questions: Mapped[List['Question']] = relationship(
        'Question', back_populates='difficulty'
    )
