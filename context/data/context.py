from __future__ import absolute_import
from datetime import datetime
import logging

from bson import ObjectId
from pylru import lrucache

from context import __version__
from context.data.base import Base
from context.settings import DATA_CACHE_SIZE_CONTEXT


class Context(Base):
    LOGGER = logging.getLogger(__name__)
    collection_name = "context"
    cache = lrucache(DATA_CACHE_SIZE_CONTEXT)

    def get(self, _id, _rev):
        if _id in self.cache and self.cache[_id]["_rev"] == _rev:
            return self.cache[_id]
        else:
            data = next(self.collection.find({"_id": _id}), None)
            self.cache[_id] = data
            return data

    def insert(self, entities, locale, new_context_id, application_id,
               session_id, user_id, now=None):
        """

        :type user_id: ObjectId
        :type session_id: ObjectId
        :type application_id: ObjectId
        :type new_context_id: ObjectId
        :type locale: str
        :type entities: list
        """
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
        self.cache[new_context_id] = record

        return {
            "_id": new_context_id,
            "_rev": new_context_id
        }

    def update(self, context_id, _rev, entities=None, now=None):

        """

        :rtype : ObjectId
        :type now: datetime
        :type entities: list
        :type _rev: ObjectId
        :type context_id: ObjectId
        """
        now = datetime.now() if now is None else now
        set_data = {
            "_rev": _rev,
            "updated": now.isoformat()
        }
        if entities is not None:
            set_data["entities"] = entities

        self.collection.update(
            {
                "_id": context_id
            },
            {
                "$set": set_data
            }
        )

        if context_id in self.cache:
            self.cache[context_id]["entities"] = entities
            self.cache[context_id]["_rev"] = _rev
            self.cache[context_id]["updated"] = now.isoformat()

        return _rev
