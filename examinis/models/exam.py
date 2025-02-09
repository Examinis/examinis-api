from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from examinis.models import Base

question_exam_association = Table(
    'question_exam',
    Base.metadata,
    Column('question_id', ForeignKey('question.id'), primary_key=True),
    Column('exam_id', ForeignKey('exam.id'), primary_key=True),
)


class Exam(Base):
    __tablename__ = 'exam'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    instructions: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship('User', back_populates='exams')
    questions: Mapped[List['Question']] = relationship(
        'Question',
        secondary=question_exam_association,
        back_populates='exams',
    )
