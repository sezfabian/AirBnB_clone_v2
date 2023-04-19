#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """This class defines a user by various attributes
    inherits from mysqlbase and links to mysql table users.

    Attributes:
        __tablename__ (str): name of mysql table to store users.
        email (sqlalchemy String) : Email of the user.
        password (sqlalchemy String) : passwd of the user.
        first_name (sqlalchemy String) : firstname of the user.
        last_name (sqlalchemy String) : lastname of the user.
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
