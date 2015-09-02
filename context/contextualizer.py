from bson.objectid import ObjectId

from context.data import MessageDirection, ContextData


class Contextualizer(object):
    def __init__(self):
        self.context_data = ContextData()
        self.context_data.open_connection()
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

    def create(self, context_id: ObjectId, user_id: ObjectId, application_id: ObjectId, session_id: ObjectId,
               locale: str) -> dict:
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

        self.context_data.insert(
            entities,
            locale,
            context_id,
            application_id,
            session_id,
            user_id
        )

    def update(self, context_id: ObjectId, _rev: ObjectId, messages: list):
        in_messages = (x for x in messages if x["direction"] == MessageDirection.IN.value)
        last_in_message = next(in_messages, None)
        existing_context = self.context_data.get(context_id, _rev)

        entities = existing_context["entities"] if existing_context is not None and "entities" in existing_context else []

        if last_in_message is not None:
            for outcome in last_in_message["detection"]["outcomes"]:
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
