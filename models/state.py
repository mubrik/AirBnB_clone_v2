#!/usr/bin/env python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

    @property
    def cities(self):
        from models import storage
        from models.city import City

        all_cities = storage.all(City)
        return [
            x for x in all_cities.values()
            if x.to_dict()['state_id'] == self.id
        ]
