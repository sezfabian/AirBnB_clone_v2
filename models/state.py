#!/usr/bin/python3
""" State Module for HBNB project """
import models
from os import getenv
from models.base_model import Base
from models.city import City
from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, base):
    """ Represents a state for a mysql database

    inherits from SQLalchemy Base and links to mysql table states.
    Attributes:
        __tablename__ (str) : The name of the mysql table to store states.
        name (sqlalchemy String) :The name of the state.
        city(sqlalchemy relationship): the state city relationship.
    """
    __tablename__ = "states"
    name = column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Get a list of all related cities."""
            city_list = []
            for city in list(models.storage.all(City).values()):
                if city.state_id = self.id:
                    city_list.append(city)
        return city_list
