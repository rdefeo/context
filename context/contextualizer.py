from collections import defaultdict
import logging
from math import sqrt

from bson.objectid import ObjectId

from pylru import FunctionCacheManager

from context.data import MessageDirection, ContextData
from context.settings import LOGGING_LEVEL
from prproc.data import AttributeProductData


class Contextualizer(object):
    logger = logging.getLogger(__name__)
    logger.setLevel(LOGGING_LEVEL)

    def __init__(self, context_data: ContextData, attribute_product_data: AttributeProductData):
        self.entity_product_count_cache = FunctionCacheManager(self.__get_entity_product_count, 1000)
        self.context_data = context_data
        self.attribute_product_data = attribute_product_data
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

    def __get_entity_product_count(self, _type, key):
        self.logger.debug("_type=%,key=%s", _type, key)
        value = self.attribute_product_data.get(_type, key, fields={"value._ids_size": True})

        return value["value"]["_ids_size"] if value is not None and "value" in value and "_ids_size" in value[
            "value"] else 0

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
        last_in_message = self.extract_last_user_message(messages)
        if last_in_message is not None:
            existing_context = self.context_data.get(context_id, _rev)
            extracted_entities = self.extract_entities(existing_context)

            entities_including_last_message = self.update_entities_with_last_message(extracted_entities,
                                                                                     last_in_message)
            entities_removing_default_if_possible = self.remove_default_entities_if_detections(
                entities_including_last_message)
            entities_with_entity_type_modified = self.create_entity_type_index_modifier(
                entities_removing_default_if_possible)
            entities_with_updated_weightings = self.change_entities_weighting(entities_with_entity_type_modified)
            entities_with_counts = self.add_product_counts(entities_with_updated_weightings)

            supported_entities, unsupported_entities = self.split_unsupported_entities(entities_with_counts)

            self.context_data.update(
                context_id,
                _rev,
                entities=supported_entities,
                unsupported_entities=unsupported_entities
            )
        else:
            self.context_data.update(context_id, _rev)

    def split_unsupported_entities(self, entities):
        supported_entities = []
        unsupported_entities = []
        for x in entities:
            if x["meta"]["instock_product_count"] == 0:
                unsupported_entities.append(x)
            else:
                supported_entities.append(x)

        return supported_entities, unsupported_entities

    def add_entity_to_context(self, entities: list, outcome_intent: str, confidence: float, _type: str, key: str):
        detection_entities = [x for x in entities if x["source"] == "detection"]
        next_entity_message_index = max([x["entity_message_index"] for x in detection_entities]) + 1 if any(
            detection_entities) else 0

        if confidence > 70.0:
            entity = {
                "key": key,
                "type": _type,
                "confidence": confidence,
                "type_weighting": self.get_global_weighting(_type),
                "source": "detection",
                "entity_message_index": next_entity_message_index
            }

            negation_modifier = -100 if outcome_intent == "exclude" or outcome_intent == "dislike" else None

            existing_entity = next((x for x in detection_entities if x["type"] == _type and x["key"] == key), None)
            if existing_entity is not None:
                existing_entity["entity_message_index"] = next_entity_message_index
                existing_entity["type_weighting"] = self.get_global_weighting(_type) * 1.1
                existing_entity["confidence"] = max(confidence, existing_entity["confidence"])
                if negation_modifier is None:
                    existing_entity.pop("negation_modifier", None)
                else:
                    existing_entity["negation_modifier"] = negation_modifier
            else:
                if negation_modifier is None:
                    entity.pop("negation_modifier", None)
                else:
                    entity["negation_modifier"] = negation_modifier
                entities.append(entity)

        return entities

    def extract_user_messages(self, messages):
        return (x for x in messages if x["direction"] == MessageDirection.IN.value)

    def extract_last_user_message(self, message):
        return next(self.extract_user_messages(message), None)

    def extract_entities(self, context):
        return context["entities"] if context is not None and "entities" in context else []

    def update_entities_with_last_message(self, entities, last_user_message):
        if last_user_message is not None:
            for outcome in last_user_message["detection"]["outcomes"]:
                for x in outcome["entities"]:
                    entities = self.add_entity_to_context(
                        entities,
                        outcome["intent"],
                        x["confidence"],
                        x["type"],
                        x["key"]
                    )
        else:
            # TODO need to decide what to do here
            pass

        return entities

    def remove_default_entities_if_detections(self, entities):
        if any(x for x in entities if x["source"] == "detection"):
            entities = [x for x in entities if x["source"] != "default"]

        return entities

    def change_entities_weighting(self, entities):
        for x in entities:
            x["weighting"] = self.calculate_weighting(x)

        return entities

    def add_product_counts(self, entities):
        for x in entities:
            x["meta"] = x["meta"] if "meta" in x else {}
            x["meta"]["instock_product_count"] = self.entity_product_count_cache(x["type"], x["key"])

        return entities

    @staticmethod
    def calculate_weighting(entity):
        weighting = entity["type_weighting"]
        weighting *= entity["confidence"] / 100 if "confidence" in entity else 1
        weighting *= entity["negation_modifier"] if "negation_modifier" in entity else 1
        weighting *= entity["type_index_modifier"] if "type_index_modifier" in entity else 1
        return weighting

    @staticmethod
    def create_entity_type_index_modifier(entities):
        new_entities = []

        type_grouping = defaultdict(list)
        for x in entities:
            type_grouping[x["type"]].append(x)

        type_grouping_with_message_index_order = {}
        for type_grouping_item in type_grouping.items():
            _type = type_grouping_item[0]
            type_grouping_with_message_index_order[_type] = defaultdict(list)
            for x in type_grouping_item[1]:
                type_grouping_with_message_index_order[_type][x["entity_message_index"]].append(x)
                pass

        for _type in type_grouping_with_message_index_order.keys():
            sorted_message_index = sorted(type_grouping_with_message_index_order[_type].keys(), reverse=True)
            for index, message_index in enumerate(sorted_message_index):
                for entity in type_grouping_with_message_index_order[_type][message_index]:
                    entity["type_index_modifier"] = 1 / sqrt(index + 1)

                    new_entities.append(entity)
        #
        #     pass
        #
        # for type_grouping_value in type_grouping.values():
        #     for index, entity in enumerate(type_grouping_value[::-1]):
        #         entity["type_index_modifier"] = 1 / sqrt(index + 1)
        #
        #         new_entities.append(entity)

        return entities
