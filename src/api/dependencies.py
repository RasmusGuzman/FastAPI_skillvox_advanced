from sqlalchemy.ext.asyncio import AsyncSession
from src.database import engine

async def get_db():
    async with AsyncSession(engine) as session:
        yield session
