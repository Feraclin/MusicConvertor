import logging

import pydantic
from sqlalchemy import URL, Result
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, sessionmaker

from api.app.config import ConfigEnv


class Base(MappedAsDataclass,
           DeclarativeBase,
           dataclass_callable=pydantic.dataclasses.dataclass):
    pass


class Database:
    def __init__(
        self,
        cfg: "ConfigEnv" = None,
    ):
        if cfg:
            self.URL_DB = URL.create(
                drivername="postgresql+asyncpg",
                host=cfg.db_host,
                database=cfg.db,
                username=cfg.db_user,
                password=cfg.db_pass,
                port=cfg.db_port,
            )
        self.engine_: AsyncEngine | None = None
        self.db_: DeclarativeBase | None = None
        self.session: AsyncSession | async_scoped_session | sessionmaker | async_sessionmaker | None = (
            None
        )
        self.logger = logging.getLogger("database")

    async def connect(self, *_: list, **__: dict) -> None:
        self.db_ = Base
        self.engine_ = create_async_engine(self.URL_DB, future=True, echo=False)
        self.session = async_sessionmaker(
            bind=self.engine_,
            expire_on_commit=False,
            autoflush=True,
        )

    async def disconnect(self, *_: list, **__: dict) -> None:
        try:
            if self.engine_:
                await self.engine_.dispose()
        except Exception as e:
            self.logger.info(f"Disconnect from engine error {e}")

    async def execute_query(self, query) -> Result:
        async with self.session() as session:
            res = await session.execute(query)
            await session.commit()
        await self.engine_.dispose()
        return res

    async def add(self, model) -> None:
        async with self.session() as session:
            session.add(model)
            await session.commit()
        await self.engine_.dispose()
