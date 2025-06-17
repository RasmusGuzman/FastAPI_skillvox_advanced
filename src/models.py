from sqlalchemy import Column, Integer, String, Text, JSON

from .database import Base
    

class Recipe(Base):
    __tablename__ = "recipes"
    
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    name: Column[str] = Column(String(100), nullable=False)
    views_count: Column[int] = Column(Integer, default=0)
    preparation_time: Column[int] = Column(Integer, nullable=False)
    ingredients: Column[dict] = Column(JSON)
    description: Column[str] = Column(Text)
