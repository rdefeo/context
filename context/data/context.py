from __future__ import absolute_import
from datetime import datetime
import logging

from bson import ObjectId

from context import __version__
from context.data.base import Base


class Context(Base):
    LOGGER = logging.getLogger(__name__)
    collection_name = "context"

    def get(self, _id, _ver):
        return self.collection.find(
            {
                "_id": _id
            }
        )[0]

    def insert(self, entities: list, locale: str, new_context_id: ObjectId, application_id: ObjectId,
               session_id: ObjectId, user_id: ObjectId, now=None):
        if now is None:
            now = datetime.now()

        record = {
            "_id": new_context_id,
            "entities": entities,
            "session_id": session_id,
            "locale": locale,
            "created": now.isoformat(),
            "application_id": application_id,
            "version": __version__,
            "_rev": new_context_id
        }
        if user_id is not None:
            record["user_id"] = user_id

        self.collection.insert(record)

        return {
            "_id": new_context_id,
            "_rev": new_context_id
        }

    def update(self, context_id: ObjectId, _ver: ObjectId, entities: list=None, now: datetime=None) -> ObjectId:

        now = datetime.now() if now is None else now
        set_data = {
            "_rev": _ver,
            "updated": now.isoformat()
        }
        if entities is not None:
            set_data["entities"] =entities


        self.collection.update(
            {
                "_id": context_id
            },
            {
                "$set": set_data
            }
        )

        return _ver
