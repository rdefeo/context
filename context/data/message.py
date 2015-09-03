from __future__ import absolute_import
import logging
from enum import Enum, unique
from datetime import datetime
from context import __version__
from bson import ObjectId

from context.data.base import Base


@unique
class Direction(Enum):
    IN = 1  # user
    OUT = 0  # jemboo


class Message(Base):
    LOGGER = logging.getLogger(__name__)
    collection_name = "message"

    def find(self, context_id=None) -> list:
        """

        :type context_id: ObjectId
        """
        query = {}
        if context_id is not None:
            query["context_id"] = context_id
        if not any(query):
            raise Exception("No parameters")
        return list(self.collection.find(query))

    def insert(self, context_id, direction, text, detection=None,
               _id=None, now=None):
        """
        :rtype : dict
        :type now: datetime
        :type _id: ObjectId
        :type detection: dict
        :type text: str
        :type direction: Direction
        :type context_id: ObjectId
        """
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

        return data

    def update(self, _id, now=None):
        """
        :type now: datetime
        :type _id: ObjectId
        """
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
