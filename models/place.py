#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
import models
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float
from os import getenv


place_amenity_table = Table("place_amenity", Base.metadata,
                            Column("place_id", String(60),
                                   ForeignKey("places.id"),
                                   primary_key=True, nullable=False),
                            Column("amenity_id", String(60),
                                   ForeignKey("amenities.id"),
                                   primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
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
    amenity_ids = []

    reviews = relationship("Review", backref="place", cascade="all, delete")

    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """
            """
            place_reviews = []
            reviews_dict = models.storage.all(Review)
            for review in reviews.values():
                if review.place_id == self.id:
                    place_reviews.append(review)

            return place_reviews

        @property
        def amenities(self):
            """
            """
            return amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """
            """
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
