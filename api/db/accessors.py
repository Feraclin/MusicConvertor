import logging

from api.db.base import Database


class BaseAccessor:

    def __init__(self, database: Database):
        self.database: Database = database
        self.logger = logging.getLogger(self.__class__.__name__)


class UserAccessor(BaseAccessor):

    def get_user(self, user_id: int) -> dict:
        pass


class RecordAccessor(BaseAccessor):
    pass




