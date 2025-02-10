from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from examinis.models import Base, question_exam_association


class Question(Base):
    __tablename__ = 'question'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    image_path: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id'))
    difficulty_id: Mapped[int] = mapped_column(ForeignKey('difficulty.id'))

    user: Mapped['User'] = relationship('User', back_populates='questions')
    subject: Mapped['Subject'] = relationship(
        'Subject', back_populates='questions'
    )
    difficulty: Mapped['Difficulty'] = relationship(
        'Difficulty', back_populates='questions'
    )
    options: Mapped[List['Option']] = relationship(
        'Option', back_populates='question'
    )
    correct_options: Mapped[List['CorrectOption']] = relationship(
        'CorrectOption', back_populates='question'
    )
    exams: Mapped[List['Exam']] = relationship(
        'Exam',
        secondary=question_exam_association,
        back_populates='questions',
    )
