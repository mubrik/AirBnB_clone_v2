#!/usr/bin/env python3
"""This module defines a class to manage db storage for hbnb clone"""
from os import environ as env
from sqlalchemy import create_engine, select, union_all
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """ DB Storage Class"""
    __engine = None
    __session = None

    def __init__(self):
        """ init method """
        username = env.get('HBNB_MYSQL_USER', None)
        password = env.get('HBNB_MYSQL_PWD', None)
        host = env.get('HBNB_MYSQL_HOST', 'localhost')
        dbname = env.get('HBNB_MYSQL_DB', None)
        if not all([username, password, host, dbname]):
            raise ValueError('Check environment variables')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                username, password, host, dbname), pool_pre_ping=True)

    def all(self, cls=None):
        """ Query the DB for all objs """
        from exports import valid_classes
        objs = {}
        if cls is None:
            # change to loop to simplify later
            for key, val in valid_classes.items():
                # skip amenities for now
                if key not in ['BaseModel', 'Amenity']:
                    for model in self.__session.query(val).all():
                        key = f'{key}.{model.id}'
                        value = model
                        objs[key] = value
        else:
            if cls.__name__ in valid_classes:
                for model in self.__session.query(val).all():
                    key = f'{cls.__name__}.{model.id}'
                    value = model
                    objs[key] = value
        return objs

    def new(self, obj):
        """ adds an obj to the session """
        from models.base_model import BaseModel

        if isinstance(obj, BaseModel):
            self.__session.add(obj)

    def save(self):
        """ commits the current session """
        self.__session.commit()

    def delete(self, obj):
        """ removes an obj from the current session """
        from models.base_model import BaseModel

        if isinstance(obj, BaseModel):
            self.__session.delete(obj)

    def reload(self):
        """ creates the tables and session """
        from models.base_model import Base

        Base.metadata.create_all(self.__engine)
        if env.get('HBNB_ENV', '') == 'test':
            Base.metadata.drop_all()
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()
