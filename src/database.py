from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

engine = create_async_engine(DATABASE_URL, echo=True)

LocalSession = sessionmaker(class_=AsyncSession, expire_on_commit=False, bind=engine)

Base = declarative_base()

def get_session():
    session = LocalSession()
    return session
