import pytest


@pytest.mark.asyncio
async def test_create_recipe(client):

    recipe_data = {
        "name": "Картофель жареный",
        "preparation_time": 30,
        "ingredients": "картошка, масло, соль",
        "description": "Простой рецепт жареной картошки."
    }
    response = client.post('/recipes/', json=recipe_data)
    assert response.status_code == 200
    created_recipe = response.json()
    assert isinstance(created_recipe['id'], int)
    assert created_recipe["name"] == "Картофель жареный"


@pytest.mark.asyncio
async def test_list_recipes(client, init_data):
    response = client.get('/recipes/')
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) >= 4


@pytest.mark.asyncio
async def test_get_recipe(client, init_data):

    response = client.get('/recipes/1')
    assert response.status_code == 200
    retrieved_recipe = response.json()
    assert retrieved_recipe["name"] == "Борщ"


@pytest.mark.asyncio
async def test_nonexistent_recipe(client):
    response = client.get('/recipes/999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Recipe not found'


@pytest.mark.asyncio
async def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert '<html>' in response.text
