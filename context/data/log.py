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

    def map_reduce_aliases(self):
        """
        Used to get the more displayed results
        :param _id_type_list: which types to consider in detection
        :return:
        """

        mapper = Code("""
            function(){
                for(var i in this.items) {
                    var item = this.items[i]
                    emit( { _id: item._id, type: "result_listing" }, 1 )
                }
            }
        """)
        reducer = Code("""
            function(key, values) {
                return Array.sum(values);
            }
        """)
        result = self.collection.map_reduce(
            mapper,
            reducer,
            query={
                "type": "results"
            },
            # out=SON(
            #     [
            #         ("replace", "aliases_attributes")
            #         # , ("db", "outdb")
            #     ]
            # )

        )

        return result