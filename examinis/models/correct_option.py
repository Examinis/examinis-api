from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from examinis.models import Base


class CorrectOption(Base):
    __tablename__ = 'correct_option'

    question_id: Mapped[int] = mapped_column(
        ForeignKey('question.id'), primary_key=True
    )
    option_id: Mapped[int] = mapped_column(
        ForeignKey('option.id'), primary_key=True
    )

    question: Mapped['Question'] = relationship(
        'Question', back_populates='correct_options'
    )
    option: Mapped['Option'] = relationship('Option')
