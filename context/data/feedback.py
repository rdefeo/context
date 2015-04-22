from __future__ import absolute_import
from datetime import datetime
import logging
from bson.code import Code
from bson.son import SON
from datetime import datetime
from datetime import datetime, timedelta
from pkg_resources import VERSION
import context
from context.data.base import Base

__author__ = 'robdefeo'


class Feedback(Base):
    LOGGER = logging.getLogger(__name__)
    collection_name = "feedback"

    def insert(self, user_id, application_id, session_id, context_id, product_id, _type, meta_data, now=None):
        if now is None:
            now = datetime.now()

        record = {
            "created": now.isoformat(),
            "application_id": application_id,
            "session_id": session_id,
            "product_id": product_id,
            "type": _type,
            "version": context.__version__
        }
        if context_id is not None:
            record["context_id"] = context_id
        if user_id is not None:
            record["user_id"] = user_id
        if meta_data is not None:
            record["meta_data"] = meta_data

        self.collection.insert(record)

    def map_product_feedback(self, now=datetime.now(), days_behind=30):
        mapper = Code("""
            function(){
                emit (
                    {
                        product_id: this.product_id
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
