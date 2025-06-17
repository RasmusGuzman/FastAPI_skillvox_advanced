from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import HTMLResponse

from . import database, models, schemas

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")


@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.post("/recipes/", response_model=schemas.RecipeOut)
async def create_recipe(
    recipe_in: schemas.RecipeIn,
        session: AsyncSession = Depends(database.get_session)
) -> models.Recipe:
    new_recipe = models.Recipe(**recipe_in.model_dump())
    async with session as sess:
        sess.add(new_recipe)
        await sess.commit()
    return new_recipe


@app.get("/recipes/", response_model=List[schemas.AllRecipeOut])
async def list_recipes(session: AsyncSession = Depends(database.get_session)):
    result = await session.execute(
        select(models.Recipe).order_by(
            models.Recipe.views_count.desc(), models.Recipe.preparation_time
        )
    )

    my_base = result.scalars().all()

    return [schemas.AllRecipeOut.model_validate(recipe) for recipe in my_base]


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
async def get_recipe(
    recipe_id: int, session: AsyncSession = Depends(database.get_session)
):
    result = await session.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.views_count += 1
    await session.commit()
    await session.refresh(recipe)

    return schemas.RecipeOut.model_validate(recipe)


@app.get("/", response_class=HTMLResponse)
async def async_start(
    request: Request, session: AsyncSession = Depends(database.get_session)
):
    return templates.TemplateResponse("base.html", {"request": request})
