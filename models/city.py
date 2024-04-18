#!/usr/bin/python3
""" City Module for HBNB project """

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import environ
from models.base_model import Base, BaseModel


class City(BaseModel, Base):
    """Defines City class that inherits from Base and BaseModel classes"""

    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")
