import pytest
from api.simple_database import SimpleDatabaseManager

def test_get_all_cars():
    db = SimpleDatabaseManager()
    cars = db.get_all_cars()
    assert isinstance(cars, list)
    assert len(cars) > 0

def test_get_cars_by_filters():
    db = SimpleDatabaseManager()
    filtered = db.get_cars_by_filters({'brand': 'Chevrolet'})
    assert isinstance(filtered, list)