from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Annotated

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

engine = create_async_engine(DATABASE_URL, echo=True)

# Объявляем явно тип LocalSession
LocalSession = Annotated[
    sessionmaker[AsyncSession],
    {"bind": engine, "class_": AsyncSession, "expire_on_commit": False},
]

Base = declarative_base()

def get_session() -> AsyncSession:
    session = LocalSession()
    return session
