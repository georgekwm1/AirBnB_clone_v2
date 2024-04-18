#!/usr/bin/python3
""" Contains the Amenity class"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from os import environ


class Amenity(BaseModel, Base):
    """Defines Amenity class"""

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship(
        "Place", secondary="place_amenity", back_populates="amenities"
        )
