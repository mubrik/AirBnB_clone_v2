#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
holds exported classes
"""

from typing import Dict, Union
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

Model_Type = Union[BaseModel, Place, City, Review, Amenity, User]

valid_classes: Dict[str, Model_Type] = {
    "BaseModel": BaseModel,
    "Place": Place,
    "City": City,
    "Review": Review,
    "Amenity": Amenity,
    "User": User,
    "State": State,
}
