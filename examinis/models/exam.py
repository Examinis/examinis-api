from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from examinis.models import Base


class Exam(Base):
    __tablename__ = 'exam'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    instructions: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship('User', back_populates='exams')
    questions: Mapped[list['Question']] = relationship(
        'Question', back_populates='exam'
    )
