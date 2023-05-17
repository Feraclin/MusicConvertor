import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship, mapped_column

from api.db.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id_: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    username: Mapped[str]
    access_token: Mapped[uuid.UUID]


class ConversationTaskModel(Base):
    __tablename__ = 'conversation_tasks'

    id_: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('users.id_', ondelete='CASCADE'))
    record_id: Mapped[uuid.UUID]
    user: Mapped[UserModel] = relationship(UserModel, lazy="joined")
