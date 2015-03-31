from __future__ import absolute_import
import logging

import pymongo
from context.data.base import Base
from bson.code import Code
from bson.son import SON
from datetime import datetime
from datetime import datetime, timedelta

TYPE_HEART = "heart"
TYPE_DETAIL = "detail"
TYPE_REMOVE = "remove"
TYPE_AFFILIATE_REDIRECT = "affiliate_redirect"


class Interest(Base):
    LOGGER = logging.getLogger(__name__)
    collection_name = "interests"

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

    def map_product_interests(self, now=datetime.now(), days_behind=30):
        mapper = Code("""
            function(){
                emit (
                    {
                        product_id: ObjectId(this.product_id)
                    },
                    {
                        affiliate_redirect_count: (this.type == "affiliate_redirect") ? 1 : 0,
                        detail_count: (this.type == "detail") ? 1 : 0,
                        heart_count: (this.type == "heart") ? 1 : 0,
                        total_count: 1
                    }
                )
            }
        """)
        reducer = Code("""
            function(key, values) {
                var result = {
                    affiliate_redirect_count: 0,
                    detail_count: 0,
                    heart_count: 0,
                    total_count: 0
                };
                values.forEach(function(value) {
                    result.affiliate_redirect_count += value.affiliate_redirect_count;
                    result.detail_count += value.detail_count;
                    result.heart_count += value.heart_count;
                    result.total_count += value.total_count;
                });

                return result;

            }
        """)

        timestamp = (now - timedelta(days=days_behind)).isoformat()

        self.LOGGER.info("generate=product_interest,updated=%s,out=product_interest,action=replace,db=generate", timestamp)

        result = self.collection.map_reduce(
            mapper,
            reducer,
            query={
                "type": {
                    "$in": [
                        "detail",
                        "heart",
                        "affiliate_redirect"
                    ]
                },
                "updated": {
                    "$gte": timestamp
                }
            },
            out=SON(
                [
                    ("replace", "product_interest"),
                    ("db", "generate")
                ]
            )

        )

        return result