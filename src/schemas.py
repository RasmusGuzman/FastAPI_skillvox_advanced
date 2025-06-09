from pydantic import BaseModel

class BaseRecipe(BaseModel):
    name: str
    preparation_time: int
    ingredients: str
    description: str

class RecipeIn(BaseRecipe):
    ...

class RecipeOut(BaseRecipe):
    ...

    class Config:
        orm_mode = True

class AllRecipeOut(BaseModel):
    name: str
    views_count: int
    preparation_time: int

    class Config:
        orm_mode = True
