import logging

import pymongo
from context.data.data import Data
from bson.code import Code
from bson.son import SON
from datetime import datetime

TYPE_HEART = "heart"


class Interest(Data):
    LOGGER = logging.getLogger(__name__)
    collection = None

    def open_connection(self):
        self.collection = self.create_db().interests

    def upsert(self, product_id, user_id, active, _type, date=None):
        self.LOGGER.info("action=interest_upserting,product_id=%s,user_id=%s", product_id, user_id)

        if date is None:
            date = datetime.now().isoformat()

        self.collection.update(
            {
                "user_id": user_id,
                "product_id": product_id,
                "type": _type
            },
            {
                "$set": {
                    "active": active,
                    "updated": date
                },
                "$setOnInsert": {
                    "user_id": user_id,
                    "product_id": product_id,
                    "type": _type,
                    "created": date
                }
            },
            upsert=True
        )