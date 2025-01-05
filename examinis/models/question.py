from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from examinis.models import Base


class Question(Base):
    __tablename__ = 'question'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id'), nullable=False)
    difficulty_id: Mapped[int] = mapped_column(ForeignKey('difficulty.id'), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='questions')
    subject: Mapped['Subject'] = relationship('Subject', back_populates='questions')
    difficulty: Mapped['Difficulty'] = relationship('Difficulty', back_populates='questions')
    options: Mapped[list['Option']] = relationship('Option', back_populates='question')
    correct_options: Mapped[list['CorrectOption']] = relationship('CorrectOption', back_populates='question')
