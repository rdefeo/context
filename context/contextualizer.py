from context.settings import CONTEXT_CACHE_SIZE

__author__ = 'robdefeo'
from bson.objectid import ObjectId
from cachetools import LRUCache
from context.data.context import Context


class Contextualizer(object):
    def __init__(self, cache_maxsize=CONTEXT_CACHE_SIZE):
        self.cache = LRUCache(maxsize=cache_maxsize, missing=self.get_from_db)
        self._global_weightings = {
            "brand": 1.0,
            "theme": 0.8,
            "style": 0.7,
            "color": 0.6,
            "detail": 0.6,
            "material": 0.5,
            "season": 0.4,
            "popular": 0.3,
            "added": 0.2
        }

    def get_global_weighting(self, _type):
        if _type in self._global_weightings:
            return self._global_weightings[_type]
        else:
            return 0.3

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

    def create(self, new_context_id, user_id, session_id, detection_result):
        # TODO get global context from DB

        context = {
            "_id": str(new_context_id)
        }
        if detection_result is None:
            context["entities"] = [
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
        elif detection_result is not None:
            entities = [
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
            for outcome in detection_result["outcomes"]:
                # if x["confidence"] > 0.6:
                for x in outcome["entities"]:
                    if x["confidence"] > 0.7:
                        weighting = self.get_global_weighting(x["type"])
                        weighting *= x["confidence"]
                        if outcome["intent"] == "exclude":
                            weighting *= -1
                        entity = {
                            "key": x["key"],
                            "type": x["type"],
                            "weighting": weighting,
                            "source": "detection"
                        }
                        entities.append(entity)
            # for x in detection_result["detections"]:
            #     entity = {
            #         "key": x["key"],
            #         "type": x["type"],
            #         "weighting": self.get_global_weighting(x["type"]),
            #         "source": "detection"
            #     }
            #     entities.append(entity)

            context["entities"] = entities
        else:
            raise NotImplemented("")

        self.cache.update(
            [
                (
                    context["_id"],
                    context
                )
            ]
        )
        return context

        # TODO get user context
        # TODO get user context
        # TODO get detection context

