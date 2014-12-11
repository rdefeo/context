import logging

import pymongo
from context.data.data import Data
from bson.code import Code
from bson.son import SON
from datetime import datetime

TYPE_HEART = "heart"
TYPE_DETAIL = "detail"
TYPE_REMOVE = "remove"

class Interest(Data):
    LOGGER = logging.getLogger(__name__)
    collection = None

    def open_connection(self):
        self.collection = self.create_db().interests

    def find(self, _type, user_id=None, session_id=None):
        if user_id is None and session_id is None:
            raise Exception("no parameters specified")

        query = {
            "type": _type,
            "active": True
        }
        if session_id is not None:
            query["session_id"] = session_id

        if user_id is not None:
            query["user_id"] = user_id

        db_items = self.collection.find(query)
        items = []
        for x in db_items:
            items.append(
                {
                    "product_id": x["product_id"],
                    "type": x["type"]
                }
            )

        return items


    def upsert(self, product_id, active, _type, user_id=None, session_id=None, date=None):
        if user_id is None and session_id is None:
            raise Exception("no parameters specified")

        if date is None:
            date = datetime.now().isoformat()

        query = {
            "type": _type,
            "product_id": product_id,
        }
        set_on_insert = {
            "product_id": product_id,
            "type": _type,
            "created": date
        }

        if session_id is not None:
            query["session_id"] = session_id
            set_on_insert["session_id"] = session_id

        if user_id is not None:
            query["user_id"] = user_id
            set_on_insert["user_id"] = user_id

        self.LOGGER.info("action=interest_upserting,product_id=%s,user_id=%s,session_id=%s", product_id, user_id, session_id)

        self.collection.update(
            query,
            {
                "$set": {
                    "active": active,
                    "updated": date
                },
                "$setOnInsert": set_on_insert
            },
            upsert=True
        )