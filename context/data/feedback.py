from datetime import datetime
import logging
from pkg_resources import VERSION
import context
from context.data.data import Data

__author__ = 'robdefeo'


class Feedback(Data):
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
