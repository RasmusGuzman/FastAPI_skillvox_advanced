from sqlalchemy import Column, Integer, String, Text, JSON

from .database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    views_count = Column(Integer, default=0)
    preparation_time = Column(Integer, nullable=False)
    ingredients = Column(JSON)
    description = Column(Text)

    
