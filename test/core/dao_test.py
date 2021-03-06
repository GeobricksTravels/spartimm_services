import unittest
from pymongo import MongoClient
from a_la_romana_services.core.dao import DAO
from a_la_romana_services.core.utils import clean_test_db
from a_la_romana_services.config import settings as s


class DAOTestCase(unittest.TestCase):

    dao = None
    config = s.test_config
    db_name = s.test_db_name

    def setUp(self):
        self.dao = DAO(self.config)
        self.client = MongoClient()
        self.db = self.client[self.db_name]
        clean_test_db()

    def tearDown(self):
        clean_test_db()

    def test_setup(self):
        self.assertIsNotNone(self.dao)
        self.assertIsNotNone(self.dao.client)
        self.assertEquals(self.dao.db_name, self.db_name)
        self.assertEquals(self.dao.users, self.config["users"])
        self.assertEquals(self.dao.activities, self.config["activities"])
        self.assertEquals(self.dao.events, self.config["events"])
        config = {}
        tmp = DAO(config)
        self.assertIsNotNone(tmp)
        self.assertIsNotNone(tmp.client)
        self.assertEquals(tmp.db_name, s.db_name)
        self.assertEquals(tmp.users, s.users)
        self.assertEquals(tmp.activities, s.activities)
        self.assertEquals(tmp.events, s.events)

    def test_create_user(self):
        user = {
            "user_id": "12345678",
            "name": "John Doe",
            "email": "something@test.com",
            "image_url": "http://www.test.com/imege.jpg"
        }
        user_id = self.dao.create_user(user)
        self.assertIsNotNone(user_id)
        user["id"] = user_id
        try:
            self.dao.create_user(user)
        except Exception, e:
            self.assertEquals(int(str(e)), 409)
        try:
            self.dao.create_user({})
        except Exception, e:
            self.assertEquals(int(str(e)), 400)
        user = {
            "_id": "507f191e810c19729de860ea",
            "user_id": "12345678",
            "name": "John Doe",
            "image_url": "http://www.test.com/imege.jpg",
            "email": "someting@example.com"
        }
        try:
            self.dao.create_user(user)
        except Exception, e:
            self.assertEquals(int(str(e)), 409)

    def test_get_user(self):
        u = self.dao.get_user('507f191e810c19729de860ea')
        self.assertIsNone(u)
        u = self.dao.get_user(None)
        self.assertEquals(u.count(), 0)
