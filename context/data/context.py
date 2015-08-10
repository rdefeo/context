from __future__ import absolute_import
from datetime import datetime
from enum import unique, Enum
import logging

from bson import ObjectId

from context import __version__
from context.data.base import Base

__author__ = 'robdefeo'


@unique
class MessageDirection(Enum):
    IN = 1
    OUT = 0


class Context(Base):
    LOGGER = logging.getLogger(__name__)
    collection_name = "context"

    def get(self, _id):
        return self.collection.find(
            {
                "_id": _id
            }
        )[0]

    def insert(self, entities, locale, new_context_id, application_id, session_id, user_id, detection_id, now=None):
        if now is None:
            now = datetime.now()

        record = {
            "_id": new_context_id,
            "entities": entities,
            "session_id": session_id,
            "locale": locale,
            "created": now.isoformat(),
            "application_id": application_id,
            "version": __version__
        }
        if user_id is not None:
            record["user_id"] = user_id
        if detection_id is not None:
            record["detection_id"] = detection_id

        self.collection.insert(record)

    def insert_message(self, context_id: ObjectId, direction: MessageDirection, text: str, detection_id: ObjectId=None,
                    _id: ObjectId=None, now: datetime=None) -> ObjectId:

        now = datetime.now() if now is None else now
        _id = ObjectId() if _id is None else _id

        data = {
            "_id": _id,
            "direction": direction.value,
            "text": text,
            "created": now.isoformat(),
            "updated": now.isoformat(),
            "version": __version__
        }

        if detection_id is not None:
            data["detection_id"] = detection_id

        self.collection.update(
            {
                "_id": context_id
            },
            {
                "$push": {
                    "messages": data
                }
            }
        )

        return _id

    def find_messages(self, context_id: ObjectId=None) -> list:
        query = {}
        if context_id is not None:
            query["_id"] = context_id

        if not any(query):
            raise Exception("No parameters")

        item = self.collection.find(query, {"messages": 1})[0]
        return item["messages"] if "messages" in item else []

