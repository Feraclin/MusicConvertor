import logging
import uuid

from sqlalchemy import select, insert

from api.app.models import UserModel, RecordModel
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

    async def get_user_by_id(self, id_: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.id_ == id_)
        res = await self.database.execute_query(query)
        return res.scalar_one_or_none()

    async def create_user(self, username) -> tuple[uuid.UUID, uuid.UUID]:
        user: UserModel = await self.get_user_by_username(username=username)
        if user:
            self.logger.info(f"{user.username} already in base")
            return user.id_, user.access_token
        else:
            user = UserModel(
                id_=uuid.uuid4(), username=username, access_token=uuid.uuid4()
            )
            await self.database.add(user)
            self.logger.info(f"{user.username} created")
            return user.id_, user.access_token


class RecordAccessor(BaseAccessor):
    async def add_record_to_db(self, user_id: str, record_id: str, title: str) -> None:
        record = insert(RecordModel).values(user_id=user_id, record_id=record_id, title=title)
        await self.database.execute_query(record)

    async def get_record_title(self, record_id: str) -> str | None:
        query = select(RecordModel.title).where(RecordModel.record_id == record_id)
        title = await self.database.execute_query(query=query)
        return title.scalar_one_or_none()

    async def get_records_list_by_user(self, user_id: str) -> list[RecordModel | None]:
        query = select(RecordModel).where(RecordModel.user_id == user_id)
        record_lst = await self.database.execute_query(query)
        return record_lst.scalars()
