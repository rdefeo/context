from __future__ import absolute_import
from datetime import datetime
import logging
import context
from context.data.base import Base

__author__ = 'robdefeo'


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
            "version": context.__version__
        }
        if user_id is not None:
            record["user_id"] = user_id
        if detection_id is not None:
            record["detection_id"] = detection_id

        self.collection.insert(record)