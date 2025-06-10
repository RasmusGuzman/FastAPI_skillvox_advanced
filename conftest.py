import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from src.main import app
from src.database import Base
from src.api.dependencies import get_db

# Тестовая база данных в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Движок и сессия для тестов
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

# Генерируем фикстуру для подготовки базы данных
@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Переопределяем зависимость get_db для тестов
@pytest.fixture(scope="function")
async def client():
    async def _override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db

    # Создаем клиент FastAPI
    async_client = TestClient(app)

    # Выполняем все запросы внутри одного контекста
    async with async_client as ac:
        yield ac

    # Возвращаемся к исходному поведению после завершения теста
    app.dependency_overrides.clear()
