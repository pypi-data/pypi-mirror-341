import yaml
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from datify import read_folder

def create_email_index(data, index):
    for person in data:
        index[person['email']] = person
    return index

def create_email_to_car_index(persons_data, cars_data, index):
    # Iterate over persons
    for person in persons_data:
        # Create an empty list for each person
        index[person['email']] = []
        # Iterate over cars
        for car in cars_data:
            # If the car owner email matches the person email, add car to index
            if car['owner']['email'] == person['email']:
                index[person['email']].append(car)
    return index

class TestDataMerge(unittest.TestCase):

    def test_read(self):

        persons_data = []
        persons_index = {}
        cars_data = []
        cars_index = {}

        read_folder(os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests/data')), 'persons', persons_data, persons_index)
        read_folder(os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests/data')), 'cars', cars_data, cars_index)

        # Resolve references manually
        for car in cars_data:
            car['owner'] = persons_index[car['owner']]

        email_index = {}
        create_email_index(persons_data, email_index)

        email_to_car_index = {}
        create_email_to_car_index(persons_data, cars_data, email_to_car_index)

        merged_data = {
            'data': {
                'persons': persons_data,
                'cars': cars_data
            },
            'indexes': {
                'persons': persons_index,
                'cars': cars_index,
                'email': email_index,
                'email_to_car': email_to_car_index
            }
        }

        # Print the merged data
        print(yaml.dump(merged_data, sort_keys=False, default_flow_style=False))
