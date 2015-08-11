from context.settings import CONTEXT_CACHE_SIZE

__author__ = 'robdefeo'
from bson.objectid import ObjectId
from cachetools import LRUCache
from context.data.context import Context


class Contextualizer(object):
    def __init__(self, cache_maxsize=CONTEXT_CACHE_SIZE):
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

    def create(self, new_context_id: ObjectId, user_id: ObjectId, session_id: ObjectId):
        context = {
            "_id": new_context_id,
            "entities": [
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
        }

        return context

    # def create(self, new_context_id, user_id, session_id, detection_result):
    #     # TODO get global context from DB
    #
    #     context = {
    #         "_id": str(new_context_id)
    #     }
    #     if detection_result is None:
    #         context["entities"] = [
    #             {
    #                 "type": "popular",
    #                 "key": "popular",
    #                 "weighting": self.get_global_weighting("popular"),
    #                 "source": "default"
    #             },
    #             {
    #                 "type": "added",
    #                 "key": "added",
    #                 "weighting": self.get_global_weighting("added"),
    #                 "source": "default"
    #             }
    #         ]
    #     elif detection_result is not None:
    #         entities = []
    #         for outcome in detection_result["outcomes"]:
    #             for x in outcome["entities"]:
    #                 if x["confidence"] > 70.0:
    #                     weighting = self.get_global_weighting(x["type"])
    #                     weighting *= (x["confidence"] / 100)
    #                     if outcome["intent"] == "exclude":
    #                         weighting *= -100
    #                     entity = {
    #                         "key": x["key"],
    #                         "type": x["type"],
    #                         "weighting": weighting,
    #                         "source": "detection"
    #                     }
    #                     entities.append(entity)
    #         # for x in detection_result["detections"]:
    #         #     entity = {
    #         #         "key": x["key"],
    #         #         "type": x["type"],
    #         #         "weighting": self.get_global_weighting(x["type"]),
    #         #         "source": "detection"
    #         #     }
    #         #     entities.append(entity)
    #
    #         context["entities"] = entities
    #     else:
    #         raise NotImplemented("")
    #
    #     self.cache.update(
    #         [
    #             (
    #                 context["_id"],
    #                 context
    #             )
    #         ]
    #     )
    #     return context
    #
    #     # TODO get user context
    #     # TODO get user context
    #     # TODO get detection context
