#!/usr/bin/python3
'''
    unnit Testing the file_storage module.
'''
import time
import unittest
import sys
from models.engine.db_storage from io import StringIO
import DBStorage
from models import storage
from models.user import User
from models.state import State
from models import storage
from console import HBNBCommand
from os import getenv


db = getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db != 'db', "Testing DBstorage only")
class test_DBStorage(unittest.TestCase):
    '''
        Testing the DB_Storage classess
    '''
    @classmethod
    def setUpClass(cls):
        '''
            Init classes
        '''
        cls.dbstorage = DBStorage()
        cls.output = StringIO()
        sys.stdout = cls.output

    @classmethod
    def tearDownClass(cls):
        '''
            delete val
        '''
        del cls.dbstorage
        del cls.output

    def create(self):
        '''
            Create HBNBCommand() line :
        '''
        return HBNBCommand()

    def test_new(self):
        '''
            Test DB new
        '''
        new_obj = State(name="California")
        self.assertEqual(new_obj.name, "California")

    def test_dbstorage_user_attr(self):
        '''
            Testing User attributes
        '''
        new = User(email="ngoni19@live.com", password="ALX!")
        self.assertTrue(new.email, "ngoni19@live.com")

    def test_dbstorage_check_method(self):
        '''
            Check methods exists
        '''
        self.assertTrue(hasattr(self.dbstorage, "all"))
        self.assertTrue(hasattr(self.dbstorage, "__init__"))
        self.assertTrue(hasattr(self.dbstorage, "new"))
        self.assertTrue(hasattr(self.dbstorage, "save"))
        self.assertTrue(hasattr(self.dbstorage, "delete"))
        self.assertTrue(hasattr(self.dbstorage, "reload"))

    def test_dbstorage_all(self):
        '''
            Testing for all function
        '''
        storage.reload()
        result = storage.all("")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
        new = User(email="toronto@gmail.com", password="yeah!")
        console = self.create()
        console.onecmd("create State name=California")
        result = storage.all("State")
        self.assertTrue(len(result) > 0)

    def test_dbstorage_new_save(self):
        '''
           Testing save method
        '''
        new_state = State(name="NewYork")
        storage.new(new_state)
        save_id = new_state.id
        result = storage.all("State")
        temp_list = []
        for x, v in result.items():
            temp_list.append(x.split('.')[1])
            obj = v
        self.assertTrue(save_id in temp_list)
        self.assertIsInstance(obj, State)

    def test_dbstorage_delete(self):
        '''
            Testing delete method
        '''
        new_user = User(email="alxo@gmail.com", password="getme!",
                        first_name="Breezy", last_name="Tolentino")
        storage.new(new_user)
        save_id = new_user.id
        key = "User.{}".format(save_id)
        self.assertIsInstance(new_user, User)
        storage.save()
        old_result = storage.all("User")
        del_user_obj = old_result[key]
        storage.delete(del_user_obj)
        new_result = storage.all("User")
        self.assertNotEqual(len(old_result), len(new_result))

    def test_model_storage(self):
        '''
            Test to check if storage --> an instance for DBStorage
        '''
        self.assertTrue(isinstance(storage, DBStorage))

    def test_db_storage_count(self):
        '''
            Check total count of objs in DBStorage
        '''
        storage.reload()
        all_count = storage.count(None)
        self.assertIsInstance(all_count, int)
        cls_count = storage.count("State")
        self.assertIsInstance(cls_count, int)
        self.assertGreaterEqual(all_count, cls_count)

    def test_db_storage_get(self):
        '''
            Check if instance gotten for DBStorage
        '''
        new_o = State(name="Cali")
        obj = storage.get("State", "fake_id")
        self.assertIsNone(obj)
