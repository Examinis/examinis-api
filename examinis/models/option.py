from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from examinis.models import Base


class Option(Base):
    __tablename__ = 'option'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    letter: Mapped[str]
    is_correct: Mapped[bool]

    question_id: Mapped[int] = mapped_column(ForeignKey('question.id'))
