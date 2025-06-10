import pytest_asyncio
from httpx import AsyncClient

from src.main import app
from src.database import Base
from src.test_database import get_async_session, test_engine, TestingSessionLocal


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """
    При сессии: создаём чистую БД перед тестами и удаляем после.
    """
    # создаём таблицы
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # чистим после себя
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_session():
    """
    Отдельная сессия для каждого теста (можно добавить rollback, если нужно).
    """
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(async_session):
    """
    HTTP-клиент httpx.AsyncClient, у которого перекрыта зависимость get_async_session.
    """
    async def override_get_async_session():
        yield async_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
