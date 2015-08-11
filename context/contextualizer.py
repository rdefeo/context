from context.settings import CONTEXT_CACHE_SIZE
from bson.objectid import ObjectId
from cachetools import LRUCache
from context.data.context import Context
from context.data import MessageDirection, ContextData


class Contextualizer(object):
    def __init__(self, cache_maxsize=CONTEXT_CACHE_SIZE):
        self.context_data = ContextData()
        self.context_data.open_connection()
        self.cache = LRUCache(maxsize=cache_maxsize, missing=self.get_from_db)
        self._global_weightings = {
            "brand": 100.0,
            "color": 90.0,
            "style": 80.0,
            "theme": 70.0,
            "season": 70.0,
            "detail": 60.0,
            "material": 50.0,
            "popular": 30.0,
            "added": 20.0
        }

    def get_global_weighting(self, _type):
        if _type in self._global_weightings:
            return self._global_weightings[_type]
        else:
            return 30.0

    def get_from_db(self, context_id):
        db = Context()
        db.open_connection()
        context = db.get(ObjectId(context_id))
        db.close_connection()
        context["_id"] = str(context["_id"])
        context["session_id"] = str(context["session_id"])
        context["application_id"] = str(context["application_id"])
        context["detection_id"] = str(context["detection_id"]) if "detection_id" in context else None
        return context

    def create(self, user_id: ObjectId, session_id: ObjectId):
        return [
            {
                "type": "popular",
                "key": "popular",
                "weighting": self.get_global_weighting("popular"),
                "source": "default"
            },
            {
                "type": "added",
                "key": "added",
                "weighting": self.get_global_weighting("added"),
                "source": "default"
            }
        ]

    def update(self, context_id: ObjectId, _rev:ObjectId, messages:list):
        in_messages = (x for x in messages if x["direction"] == MessageDirection.IN)
        last_in_message = next(in_messages, None)
        entities = []
        if last_in_message is not None:
            for outcome in last_in_message["outcomes"]:
                for x in outcome["entities"]:
                    if x["confidence"] > 70.0:
                        weighting = self.get_global_weighting(x["type"])
                        weighting *= (x["confidence"] / 100)
                        if outcome["intent"] == "exclude":
                            weighting *= -100
                        entity = {
                            "key": x["key"],
                            "type": x["type"],
                            "weighting": weighting,
                            "source": "detection"
                        }
                        entities.append(entity)
        else:
            # TODO need to decide what to do here
            pass

        self.context_data.update(context_id, _rev, entities=entities)
        return entities
