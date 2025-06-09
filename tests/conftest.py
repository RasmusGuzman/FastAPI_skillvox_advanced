import pytest
from fastapi.testclient import TestClient
from src.database import Base
from src.main import app
from src.models import Recipe
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:" 


test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="module")
async def db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield TestSessionLocal()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
async def init_data(db):
    async with db as session:
        recipes = [
            Recipe(name="Борщ", preparation_time=60, ingredients="Свёкла, морковь, картофель", description="Классический борщ"),
            Recipe(name="Паста Карбонара", preparation_time=30, ingredients="Спагетти, яйца, сыр", description="Итальянская классика"),
            Recipe(name="Салат Цезарь", preparation_time=20, ingredients="Куриное филе, листья салата", description="Американский салат"),
            Recipe(name="Сырники", preparation_time=25, ingredients="Творог, яйцо, мука", description="Традиционное блюдо русской кухни")
        ]
        session.add_all(recipes)
        await session.commit()
        await session.refresh(recipes)
        yield db
