#!/usr/bin/python3
""" Place Module for HBNB project """

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review
import models
from os import environ


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False,
    ),
)


class Place(BaseModel, Base):
    """defines the Place class"""
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship(
            "Amenity",
            secondary="place_amenity",
            viewonly=False,
            back_populates="place_amenities",
            )
    # else:
    #     city_id = ""
    #     user_id = ""
    #     name = ""
    #     description = ""
    #     number_rooms = 0
    #     number_bathrooms = 0
    #     max_guest = 0
    #     price_by_night = 0
    #     latitude = 0.0
    #     longitude = 0.0
    #     amenity_ids = []

    #     @property
    #     def reviews(self):
    #         return [
    #             item for item in models.storage.all(Review).values()
    #             if item.place_id == self.id
    #         ]

    #     @property
    #     def amenities(self):
    #         return [
    #             item for item in models.storage.all(Amenity).values()
    #             if item.id in self.amenity_ids
    #         ]

    #     @amenities.setter
    #     def amenities(self, obj):
    #         if isinstance(obj, Amenity):
    #             self.amenity_ids.append[obj]
