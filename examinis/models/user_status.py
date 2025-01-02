from sqlalchemy.orm import Mapped, mapped_column, relationship

from examinis.models import Base


class UserStatus(Base):
    __tablename__ = 'user_status'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    users: Mapped[list['User']] = relationship('User', back_populates='status')
