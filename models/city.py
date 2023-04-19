#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """ The city class
    Attributes:
        state ID: state id
        name: city name """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(128), nullable=False, ForeignKey('states.id'))
