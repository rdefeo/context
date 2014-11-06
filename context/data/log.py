__author__ = 'robdefeo'
import logging

import pymongo
from context.data.data import Data
from bson.code import Code
from bson.son import SON
from datetime import datetime


class Log(Data):
    LOGGER = logging.getLogger(__name__)
    collection = None

    def open_connection(self):
        self.collection = self.create_db().logs

    def insert(self, _type, payload):
        data = payload
        data["type"] = _type
        self.collection.insert(
            data
        )