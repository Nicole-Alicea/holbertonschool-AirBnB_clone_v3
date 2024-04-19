#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state_data = {'name': 'Florida'}
        new_state = State(**state_data)

        models.storage.new(new_state)
        models.storage.save()

        session = models.storage._DBStorage__session

        all_obj = session.query(State).all()

        self.assertTrue(len(all_obj) > 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        state_data = {'name': 'Georgia'}
        new_state = State(**state_data)

        models.storage.new(new_state)

        session = models.storage._DBStorage__session

        provided_state = session.query(State).filter_by(id=new_state.id).first()  # noqa

        self.assertEqual(provided_state.id, new_state.id)
        self.assertEqual(provided_state.name, new_state.name)
        self.assertIsNotNone(provided_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state_data = {'name': 'New York'}
        new_state = State(**state_data)

        models.storage.new(new_state)
        models.storage.save()

        session = models.storage._DBStorage__session

        provided_state = session.query(State).filter_by(id=new_state.id).first()  # noqa

        self.assertEqual(provided_state.id, new_state.id)
        self.assertEqual(provided_state.name, new_state.name)
        self.assertIsNotNone(provided_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Will test the method for obtaining an instance of db storage"""
        storage = models.storage
        storage.reload()

        state_data = {'name': 'Utah'}
        instance = State(**state_data)
        storage.new(instance)
        storage.save()

        provided_state = storage.get(State, instance.id)

        self.assertEqual(instance, provided_state)

        fake_id = storage.get(State, 'fake_state_id')

        self.assertEqual(fake_id, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Will test the method for obtaining all instances of db storage"""
        storage = models.storage
        storage.reload()

        state_data = {'name': 'California'}
        instance = State(**state_data)
        storage.new(instance)

        city_data = {'name': 'Los Angeles', 'state_id': instance.id}
        city_instance = City(**city_data)

        storage.new(city_instance)
        storage.save()

        state_instances = storage.count(State)
        self.assertEqual(state_instances, len(storage.all(State)))

        all_instances = storage.count()
        self.assertEqual(all_instances, len(storage.all()))
