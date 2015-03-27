from datetime import datetime
import logging
from context.data.data import Data

__author__ = 'robdefeo'

class Context(Data):
    LOGGER = logging.getLogger(__name__)
    collection_name = "contexts"

    def get(self, _id):
        return self.collection.find(
            {
                "_id": _id
            }
        )[0]

    def insert(self, entities, locale, new_context_id, application_id, session_id, user_id, detection_id, now=None):
        if now is None:
            now = datetime.now()

        self.collection.insert(
            {
                "_id": new_context_id,
                "entities": entities,
                "user_id": user_id,
                "detection_id": detection_id,
                "session_id": session_id,
                "locale": locale,
                "created": now.isoformat(),
                "application_id": application_id
            }
        )