#!/usr/bin/env python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True)
    created_at = Column(Date, default=datetime.now(), nullable=False)
    updated_at = Column(Date, default=datetime.now(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        self.id = str(uuid.uuid4())
        now = datetime.now()
        self.created_at = now
        self.updated_at = now
        date_f = '%Y-%m-%dT%H:%M:%S.%f'
        ignore = {'__class__', 'created_at', 'updated_at'}
        attrs = {k: v for k, v in kwargs.items() if k not in ignore}
        for attr, value in attrs.items():
            setattr(self, attr, value)
        if 'created_at' in kwargs:
            self.created_at = datetime.strptime(kwargs['created_at'], date_f)
        if 'updated_at' in kwargs:
            self.updated_at = datetime.strptime(
                kwargs['updated_at'], date_f)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(
            cls, self.id, {
                k: v for k, v in self.to_dict().items() if k != '__class__'})

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """ delete insatnce from storage """
        from models import storage
        storage.delete(self)
