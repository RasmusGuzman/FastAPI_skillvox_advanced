from pydantic import BaseModel, ConfigDict

class BaseRecipe(BaseModel):
    name: str
    preparation_time: int
    ingredients: list[str]
    description: str

    model_config = ConfigDict(from_attributes=True)
    
class RecipeIn(BaseRecipe):
    ...

class RecipeOut(BaseModel):
    name: str
    views_count: int
    preparation_time: int

    class Config:
        orm_mode = True

class AllRecipeOut(BaseModel):
    name: str
    views_count: int
    preparation_time: int

    class Config:
        orm_mode = True
