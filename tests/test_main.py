# test_main.py

import pytest

@pytest.mark.asyncio
async def test_create_recipe(client):
    response = await client.post("/recipes/", json={
        "name": "Борщ",
        "preparation_time": 30,
        "ingredients": ["Свёкла", "Картофель"],
        "description": "Традиционный русский суп."
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Борщ"

@pytest.mark.asyncio
async def test_list_recipes(client):
    response = await client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_nonexistent_recipe(client):
    response = await client.get("/recipes/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"

@pytest.mark.asyncio
async def test_homepage(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "<html>" in response.text
