import logging
from typing import Optional

from fastapi import FastAPI

from api.app.api_v1.deps import app_dependency, user_dependency
from api.app.api_v1.routers import api_routers
from api.app.config import ConfigEnv, config_api
from api.db.accessors import UserAccessor, RecordAccessor
from api.db.base import Database


class AppState:
    def __init__(self):
        self.database: Optional[Database] = None
        self.config: Optional[ConfigEnv] = None
        self.users: Optional[UserAccessor] = None
        self.records: Optional[RecordAccessor] = None
        self.logger: Optional[logging.Logger] = None


class Application(FastAPI):
    state: Optional[AppState] = None


app = Application()
app.state = AppState()


@app.on_event("startup")
async def startup_event():
    app.state.config = config_api
    database = Database(app.state.config)
    await database.connect()

    app.state.database = database
    app.state.users = UserAccessor(database)
    app.state.records = RecordAccessor(database)
    app.state.logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_event():
    database = app.state.database
    if database:
        await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(
    router=api_routers, prefix="/api_v1", dependencies=[app_dependency]
)
