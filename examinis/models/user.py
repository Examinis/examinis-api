from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from examinis.models import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    status_id: Mapped[int] = mapped_column(ForeignKey('user_status.id'))
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'))

    status: Mapped['UserStatus'] = relationship(
        'UserStatus', back_populates='users'
    )
    role: Mapped['Role'] = relationship('Role', back_populates='users')
    questions: Mapped[List['Question']] = relationship(
        'Question', back_populates='user'
    )
    exams: Mapped[List['Exam']] = relationship('Exam', back_populates='user')
