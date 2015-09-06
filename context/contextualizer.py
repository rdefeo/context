from collections import defaultdict
from math import sqrt

from bson.objectid import ObjectId

from context.data import MessageDirection, ContextData


class Contextualizer(object):
    def __init__(self, context_data: ContextData):
        self.context_data = context_data
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
                "type_weighting": self.get_global_weighting("popular"),
                "source": "default"
            },
            {
                "type": "added",
                "key": "added",
                "type_weighting": self.get_global_weighting("popular"),
                "source": "default"
            }
        ]

        for x in entities:
            x["weighting"] = self.calculate_weighting(x)

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

        entities = existing_context[
            "entities"] if existing_context is not None and "entities" in existing_context else []
        detection_entities = [x for x in entities if x["source"] == "detection"]
        next_entity_message_index = max([x["entity_message_index"] for x in detection_entities]) + 1 if any(
            detection_entities) else 0

        if last_in_message is not None:
            for outcome in last_in_message["detection"]["outcomes"]:
                for x in outcome["entities"]:
                    if x["confidence"] > 70.0:
                        entity = {
                            "key": x["key"],
                            "type": x["type"],
                            "confidence": x["confidence"],
                            "type_weighting": self.get_global_weighting(x["type"]),
                            "source": "detection",
                            "entity_message_index": next_entity_message_index
                        }
                        if outcome["intent"] == "exclude":
                            entity["negation_modifier"] = -100

                        entities.append(entity)
        else:
            # TODO need to decide what to do here
            pass

        if any(x for x in entities if x["source"] != "detection"):
            entities = [x for x in entities if x["source"] != "default"]

        entities = self.create_entity_type_index_modifier(entities)

        for x in entities:
            x["weighting"] = self.calculate_weighting(x)
            pass

        self.context_data.update(context_id, _rev, entities=entities)
        return entities

    def calculate_weighting(self, entity):
        weighting = entity["type_weighting"]
        weighting *= entity["confidence"] / 100 if "confidence" in entity else 1
        weighting *= entity["negation_modifier"] if "negation_modifier" in entity else 1
        weighting *= entity["type_index_modifier"] if "type_index_modifier" in entity else 1
        return weighting

    def create_entity_type_index_modifier(self, entities):
        type_grouping = defaultdict(list)
        for x in entities:
            type_grouping[x["type"]].append(x)

        new_entities = []
        for value in type_grouping.values():
            for index, entity in enumerate(value[::-1]):
                entity["type_index_modifier"] = 1 / sqrt(index + 1)

                new_entities.append(entity)

        return entities
