#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id")),
    Column("amenity_id", String(60), ForeignKey("amenities.id")),
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenities = relationship(
        "Amenity", secondary=place_amenity, viewonly=False, backref="amenities"
    )
    amenity_ids = []
    reviews = relationship('Review', backref='place', cascade='all, delete')

    @property
    def reviews(self):
        """ getter for file storage """
        from models import storage
        from models.review import Review

        all_reviews = storage.all(Review)
        return [
            x for x in all_reviews.values()
            if x.to_dict()['place_id'] == self.id
        ]

    @property
    def amenities(self):
        """ getter for file storage """
        from models import storage
        from models.amenity import Amenity

        all_amenities = storage.all(Amenity)
        return [
            x for x in all_amenities.values()
            if x.to_dict()['id'] in self.amenity_ids
        ]

    @amenities.setter
    def amenities(self, obj):
        """ setter for file storage """
        from models import storage
        from models.amenity import Amenity

        if isinstance(obj, Amenity):
            self.amenity_ids.append(obj.id)
