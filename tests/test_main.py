import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_root(ac: AsyncClient, prepare_database):
    response = await ac.get("/")
    assert response.status_code == 200
    assert "<h1>Welcome to best recipes library!!</h1>" in response.text



@pytest.mark.asyncio
async def test_create_recipe(aс, prepare_database):
    response = await ac.post("/recipes/", json={
        "name": "Борщ",
        "preparation_time": 30,
        "ingredients": ["Свёкла", "Картофель"],
        "description": "Традиционный русский суп."
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Борщ"

@pytest.mark.asyncio
async def test_list_recipes(ac, prepare_database):
    response = await ac.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_nonexistent_recipe(ac, prepare_database):
    response = await ac.get("/recipes/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"

@pytest.mark.asyncio
async def test_homepage(ac, prepare_database):
    response = await ac.get("/")
    assert response.status_code == 200
    assert "html>" in response.text.split()
