from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from starlette.responses import HTMLResponse

from . import models
from . import schemas
from . import database

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await database.session.close()
    await database.engine.dispose()


@app.post("/recipes/", response_model=schemas.RecipeOut)
async def create_recipe(recipe_in: schemas.RecipeIn) -> models.Recipe:
    new_recipe = models.Recipe(**recipe_in.dict())
    async with database.session as sess:
        sess.add(new_recipe)
        await sess.commit()
    return new_recipe


@app.get("/recipes/", response_model=List[schemas.AllRecipeOut])
async def list_recipes():
    result = await database.session.execute(
        select(models.Recipe).order_by(
            models.Recipe.views_count.desc(), models.Recipe.preparation_time
        )
    )

    my_base = result.scalars().all()

    return [
        {
            "name": recipe.name,
            "views_count": recipe.views_count,
            "preparation_time": recipe.preparation_time,
        }
        for recipe in my_base
    ]


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
async def get_recipe(recipe_id: int):
    result = await database.session.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    if recipe is None:

        raise HTTPException(status_code=404, detail="Recipe not found")
    else:
        recipe.views_count += 1
        async with database.session as sess:
            await sess.commit()

        data = {
            "name": recipe.name,
            "preparation_time": recipe.preparation_time,
            "ingredients": recipe.ingredients,
            "description": recipe.description,
        }

    return data


@app.get("/", response_class=HTMLResponse)
async def async_start(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
