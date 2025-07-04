import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.database import Base, get_session
from src.database_for_tests import test_engine, TestingSessionLocal

@pytest_asyncio.fixture(autouse=True, scope="session")
def _override_get_session():
    async def _get_test_session():
        async with TestingSessionLocal() as session:
            yield session
    app.dependency_overrides[get_session] = _get_test_session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture

async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
