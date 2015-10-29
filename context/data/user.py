from __future__ import absolute_import
import logging
from bson import ObjectId
from bson.code import Code
from bson.son import SON
from datetime import datetime, timedelta
from context import __version__
from context.data.base import Base


class User(Base):
    LOGGER = logging.getLogger(__name__)
    collection_name = "user"

    def upsert_with_facebook_data(self, user_id, facebook_userID, now=None):
        """

        :type now: datetime
        """
        now = now.isoformat()  if now is not None else datetime.now().isoformat()

        # TODO needs to deal with people logging out
        doc = self.collection.find_and_modify(
            {
                "facebook.user_id": facebook_userID
            },
            {
                "$setOnInsert": {
                    "created": now,
                    "facebook.user_id": facebook_userID
                },
                "$set": {
                    "updated": now
                }
            },
            upsert=True,
            new=True
        )

        return doc

