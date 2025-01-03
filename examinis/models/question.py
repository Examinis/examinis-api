from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from examinis.models import Base


class Question(Base):
    __tablename__ = 'question'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]

    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id'), nullable=False)
    difficulty_id: Mapped[int] = mapped_column(ForeignKey('difficulty.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    subject: Mapped['Subject'] = relationship('Subject', back_populates='questions')
    difficulty: Mapped['Difficulty'] = relationship('Difficulty', back_populates='questions')
    user: Mapped['User'] = relationship('User', back_populates='questions')
    options: Mapped[list['Option']] = relationship('Option', back_populates='question')
