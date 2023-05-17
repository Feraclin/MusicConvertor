import logging
import uuid

from sqlalchemy import select

from api.app.models import UserModel
from api.db.base import Database


class BaseAccessor:

    def __init__(self, database: Database):
        self.database: Database = database
        self.logger = logging.getLogger(self.__class__.__name__)


class UserAccessor(BaseAccessor):

    async def get_user_by_username(self, username: int) -> UserModel | None:
        query = select(UserModel).where(UserModel.username == username)
        res = await self.database.execute_query(query)
        return res.scalar_one_or_none()

    async def create_user(self, username) -> tuple[uuid.UUID, uuid.UUID]:
        user: UserModel = await self.get_user_by_username(username=username)
        if user:
            return user.id_, user.access_token
        else:
            user = UserModel(id_=uuid.uuid4(),
                             username=username,
                             access_token=uuid.uuid4())
            await self.database.add(user)
            return user.id, user.uuid


class RecordAccessor(BaseAccessor):
    pass




