#!/usr/bin/env python3
""" Test delete feature
"""
from models.engine.file_storage import FileStorage
from models.state import State
from models.city import City

fs = FileStorage()

# All Items
all_items = fs.all()
print("All Items: {}".format(len(all_items.keys())))
for state_key in all_items.keys():
    print(all_items[state_key])

# Create a new State
new_state = State()
new_state.name = "California"
fs.new(new_state)
fs.save()
print("New State: {}".format(new_state))

# Create another State
another_state = State()
another_state.name = "Nevada"
fs.new(another_state)
fs.save()
print("Another State: {}".format(another_state))

# Create a City
new_city = City()
new_city.name = "Ikeja"
fs.new(new_city)
fs.save()
print("New City: {}".format(new_city))

# All Items
all_items = fs.all()
print("All Items: {}".format(len(all_items.keys())))
for state_key in all_items.keys():
    print(all_items[state_key])

# Delete the new State
fs.delete(new_state)

# All Items
all_items = fs.all()
print("All Items: {}".format(len(all_items.keys())))
for state_key in all_items.keys():
    print(all_items[state_key])

# Delete the new City
fs.delete(new_city)

# All Items
all_items = fs.all()
print("All Items: {}".format(len(all_items.keys())))
for state_key in all_items.keys():
    print(all_items[state_key])

# Delete the new State
fs.delete(another_state)

# All Items
all_items = fs.all()
print("All Items: {}".format(len(all_items.keys())))
for state_key in all_items.keys():
    print(all_items[state_key])

fs.save()
