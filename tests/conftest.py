import pytest
from fastapi.testclient import TestClient
from src.database import engine, async_session, Base
from src.main import app
from src.models import Recipe


@pytest.fixture(scope="module")
async def db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_session()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
async def init_data(db):
    async with db as session:
        recipes = [
            Recipe(
                name="Борщ",
                preparation_time=60,
                ingredients="Свёкла, морковь, картофель",
                description="Классический борщ украинской кухни"
            ),
            Recipe(
                name="Паста Карбонара",
                preparation_time=30,
                ingredients="Спагетти, яйца, пармезан, гуанчале",
                description="Итальянская паста с яйцом и сыром"
            ),
            Recipe(
                name="Салат Цезарь",
                preparation_time=20,
                ingredients="Куриная грудка, листья салата, соус цезарь",
                description="Классический американский салат"
            ),
            Recipe(
                name="Сырники",
                preparation_time=25,
                ingredients="Творог, мука, яйца, сахар",
                description="Русские творожные оладьи"
            )
        ]
        for i_rec in recipes:
            session.add(i_rec)

        await session.commit()
        await session.refresh(recipes)
        yield db
