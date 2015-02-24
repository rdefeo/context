__author__ = 'robdefeo'
import logging

import pymongo
from context.data.data import Data
from bson.code import Code
from bson.son import SON
from datetime import datetime, timedelta


class Log(Data):
    LOGGER = logging.getLogger(__name__)
    collection_name = "logs"

    def insert(self, _type, payload):
        data = payload
        data["type"] = _type
        self.collection.insert(
            data
        )

    def map_product_result_listing(self, now=datetime.now(), days_behind=30):
        """
        Used to get the more displayed results
        :param _id_type_list: which types to consider in detection
        :return:
        """

        mapper = Code("""
            function(){
                for(var i in this.items) {
                    var item = this.items[i]
                    emit(
                        {
                            _id: ObjectId(item._id),
                            type: "result_listing"
                        },
                        1
                    )
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
                "type": "results",
                "timestamp": {
                    "$gte": (now - timedelta(days=days_behind)).isoformat()
                }
            },
            out=SON(
                [
                    ("replace", "product_result_listing"),
                    ("db", "suggest")
                ]
            )

        )

        return result