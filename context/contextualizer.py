__author__ = 'robdefeo'
from bson.objectid import ObjectId
from cachetools import LRUCache, lru_cache

class Contextualizer(object):
    def __init__(self, cache_maxsize=512):
        self.cache = LRUCache(maxsize=cache_maxsize, missing=self.get_from_db)
        # self.cache

    def get_from_db(self, context_id):
        raise NotImplemented()
        pass

    def create(self, user_id, session_id, detection_result):
        # TODO get global context
        if detection_result is None:
            context_id = ObjectId()
            self.cache.update([
                (str(context_id),
                {
                    "entities": [
                        {
                            "type": "popular",
                            "key": "popular",
                            "weighting": 1.0
                        }
                    ]
                })]
            )
            return context_id
            # return {
            #     "_id": str(ObjectId()),
            #     "entities": [
            #         {
            #             "type": "popular",
            #             "key": "popular",
            #             "weighting": 1.0
            #         }
            #     ]
            # }
        else:
            raise NotImplemented("")

        # TODO get user context
        # TODO get user context
        # TODO get detection context