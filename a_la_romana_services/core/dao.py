from pymongo import MongoClient
from bson.objectid import ObjectId


class DAO:

    # Internal parameters.
    db_name = None
    users = None
    activities = None
    events = None
    client = None
    db = None

    def __init__(self, config):
        try:
            self.db_name = 'a_la_romana_db' if config['db_name'] is None else config['db_name']
        except KeyError:
            self.db_name = 'a_la_romana_db'
        try:
            self.users = 'users' if config['users'] is None else config['users']
        except KeyError:
            self.users = 'users'
        try:
            self.activities = 'activities' if config['activities'] is None else config['activities']
        except KeyError:
            self.activities = 'activities'
        try:
            self.events = 'events' if config['events'] is None else config['events']
        except KeyError:
            self.events = 'events'
        self.client = MongoClient()
        self.db = self.client[self.db_name]

    def get_user(self, user_id):
        collection = self.db[self.users]
        if user_id is not None:
            return collection.find_one({'_id': ObjectId(user_id)})
        else:
            return collection.find()
