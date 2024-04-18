#!/usr/bin/python3
"""Contains the class State"""

from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.city import City
from os import environ
import models


class State(BaseModel, Base):
    """State class that inherites from Base and BaseModel classes"""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    # name = ""
    # @property
    # def cities(self):
    #     return [
    #         city for city in models.storage.all(City).values()
    #         if city.state_id == self.id
    #     ]
