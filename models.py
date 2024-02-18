import datetime
import os

from sqlalchemy import DateTime, String, func
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship

import sqlalchemy as sq
from typing import List

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    sticker: Mapped[List["Sticker"]] = relationship(back_populates= "user")
    @property
    def dict(self):
        return {
            "name": self.name,
            "registration_time": int(self.registration_time.timestamp()),
        }

class Sticker(Base):

    __tablename__ = "app_sticker"

    id: Mapped[int] = mapped_column(primary_key= True)
    name: Mapped[str] = mapped_column(String(50), unique= True, index= True, nullable= False)
    description: Mapped[str] = mapped_column (String(300), nullable= False)
    create_at: Mapped[datetime.datetime] = mapped_column(DateTime,server_default= func.now(), server_onupdate= func.now())
    owner: Mapped[int] = mapped_column(sq.ForeignKey("app_user.id"), nullable= False)
    user: Mapped["User"] = relationship(back_populates= "sticker")

    @property
    def dict(self):
        return {
            "id_st":self.id,
            "name_st":self.name,
            "description_st":self.description,
            "owner_st": self.owner
        }

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
