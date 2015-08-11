from __future__ import absolute_import
import logging
from enum import Enum, unique
from datetime import datetime
from context import __version__
from bson import ObjectId

from context.data.base import Base


@unique
class Direction(Enum):
    IN = 1
    OUT = 0


class Message(Base):
    LOGGER = logging.getLogger(__name__)
    collection_name = "message"

    def find(self, context_id: ObjectId=None) -> list:
        query = {}
        if context_id is not None:
            query["context_id"] = context_id
        if not any(query):
            raise Exception("No parameters")
        return list(self.collection.find(query))

    def insert(self, context_id: ObjectId, direction: Direction, text: str, detection: dict=None, _id: ObjectId=None, now: datetime=None) -> ObjectId:
        now = datetime.now() if now is None else now

        _id = ObjectId() if _id is None else _id

        data = {
            "_id": _id,
            "context_id": context_id,
            "direction": direction.value,
            "text": text,
            "created": now.isoformat(),
            "updated": now.isoformat(),
            "version": __version__
        }
        if detection is not None:
            data["detection"] = detection

        self.collection.insert(data)

        return _id

    def update(self, _id: ObjectId, now: datetime=None):
        now = datetime.now() if now is None else now

        self.collection.update(
            {
                "_id": _id
            },
            {
                "$set": {
                    "updated": now.isoformat()
                }
            }
        )
