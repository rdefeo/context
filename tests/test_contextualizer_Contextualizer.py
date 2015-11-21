__author__ = 'robdefeo'
from unittest import TestCase

from mock import MagicMock, call

from context.contextualizer import Contextualizer as Target


class add_entity_to_context_tests(TestCase):
    def test_empty_entities(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.add_entity_to_context(
            [],
            "include",
            80.0,
            "type_key",
            "key_key"
        )

        self.assertEqual(
            [
                {
                    'confidence': 80.0,
                    'entity_message_index': 0,
                    'key': 'key_key',
                    'source': 'detection',
                    'type': 'type_key',
                    'type_weighting': 30.0
                }
            ],
            actual
        )

    def test_entities(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.add_entity_to_context(
            [
                {
                    "key": "existing_key",
                    "type": "existing_key",
                    "source": "detection",
                    "entity_message_index": 0
                }

            ],
            "include",
            80.0,
            "new_key",
            "new_key"
        )

        self.assertEqual(
            [
                {
                    'entity_message_index': 0,
                    'key': 'existing_key',
                    'source': 'detection',
                    'type': 'existing_key'
                },
                {
                    'confidence': 80.0,
                    'entity_message_index': 1,
                    'key': 'new_key',
                    'source': 'detection',
                    'type': 'new_key',
                    'type_weighting': 30.0
                }
            ],
            actual
        )

    def test_existing_entity(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.add_entity_to_context(
            [
                {
                    "key": "existing_key",
                    'confidence': 80.0,
                    "type": "existing_key",
                    "source": "detection",
                    "entity_message_index": 0,
                    'type_weighting': 30.0
                }

            ],
            "include",
            80.0,
            "existing_key",
            "existing_key"
        )

        self.assertEqual(
            [
                {
                    'entity_message_index': 1,
                    'key': 'existing_key',
                    'confidence': 80.0,
                    'source': 'detection',
                    'type': 'existing_key',
                    'type_weighting': 33.0
                }
            ],
            actual
        )

    def test_existing_include_entity_now_exclude(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.add_entity_to_context(
            [
                {
                    "key": "existing_key",
                    'confidence': 80.0,
                    "type": "existing_key",
                    "source": "detection",
                    "entity_message_index": 0,
                    'type_weighting': 30.0
                }

            ],
            "exclude",
            80.0,
            "existing_key",
            "existing_key"
        )

        self.assertEqual(
            [
                {
                    'entity_message_index': 1,
                    'key': 'existing_key',
                    'confidence': 80.0,
                    'negation_modifier': -100,
                    'source': 'detection',
                    'type': 'existing_key',
                    'type_weighting': 33.0
                }
            ],
            actual
        )

    def test_existing_exclude_entity_now_include(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.add_entity_to_context(
            [
                {
                    'confidence': 80.0,
                    'entity_message_index': 1,
                    'negation_modifier': -100,
                    'key': 'black',
                    'source': 'detection',
                    'type': 'color',
                    'type_weighting': 90.0
                }

            ],
            "include",
            80.0,
            "color",
            "black"
        )

        self.assertEqual(
            [
                {
                    'confidence': 80.0,
                    'entity_message_index': 2,
                    'key': 'black',
                    'source': 'detection',
                    'type': 'color',
                    'type_weighting': 99.00000000000001
                }
            ],
            actual
        )

    def test_existing_exclude_entity(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.add_entity_to_context(
            [
                {
                    'confidence': 80.0,
                    'entity_message_index': 1,
                    'negation_modifier': -100,
                    'key': 'black',
                    'source': 'detection',
                    'type': 'color',
                    'type_weighting': 90.0
                }

            ],
            "exclude",
            80.0,
            "color",
            "black"
        )

        self.assertEqual(
            [
                {
                    'confidence': 80.0,
                    'entity_message_index': 2,
                    'negation_modifier': -100,
                    'key': 'black',
                    'source': 'detection',
                    'type': 'color',
                    'type_weighting': 99.00000000000001
                }
            ],
            actual
        )

    def test_outcome_exclude_entities(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.add_entity_to_context(
            [
                {
                    "key": "existing_key",
                    "type": "existing_key",
                    "source": "detection",
                    "entity_message_index": 0
                }

            ],
            "exclude",
            80.0,
            "new_key",
            "new_type"
        )

        self.assertEqual(
            [
                {
                    'entity_message_index': 0,
                    'key': 'existing_key',
                    'source': 'detection',
                    'type': 'existing_key'
                },
                {
                    'confidence': 80.0,
                    'entity_message_index': 1,
                    'negation_modifier': -100,
                    'key': 'new_type',
                    'source': 'detection',
                    'type': 'new_key',
                    'type_weighting': 30.0
                }
            ],
            actual
        )

    def test_low_confidence_entities(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.add_entity_to_context(
            [
                {
                    "key": "existing_key",
                    "type": "existing_key",
                    "source": "detection",
                    "entity_message_index": 0
                }

            ],
            "include",
            40.0,
            "new_key",
            "new_key"
        )

        self.assertEqual(
            [
                {
                    'entity_message_index': 0,
                    'key': 'existing_key',
                    'source': 'detection',
                    'type': 'existing_key'
                }
            ],
            actual
        )


class create_tests(TestCase):
    def test_regular(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        target.create("context_id_key", "user_id_key", "application_id_key", "session_id_key", "locale_key")

        self.assertEqual(1, context_data.insert.call_count)
        self.assertListEqual(
            [
                {'type': 'popular', 'key': 'popular', 'source': 'default', 'weighting': 30.0, 'type_weighting': 30.0},
                {'type': 'added', 'key': 'added', 'source': 'default', 'weighting': 30.0, 'type_weighting': 30.0}
            ]
            , context_data.insert.call_args_list[0][0][0])
        self.assertEqual("locale_key", context_data.insert.call_args_list[0][0][1])
        self.assertEqual("context_id_key", context_data.insert.call_args_list[0][0][2])
        self.assertEqual("application_id_key", context_data.insert.call_args_list[0][0][3])
        self.assertEqual("session_id_key", context_data.insert.call_args_list[0][0][4])
        self.assertEqual("user_id_key", context_data.insert.call_args_list[0][0][5])


class create_entity_type_index_modifier_tests(TestCase):
    def test_empty_entities(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.create_entity_type_index_modifier([])

        self.assertListEqual(
            [],
            actual
        )

    def test_single_entity(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.create_entity_type_index_modifier(
            [
                {
                    "key": "color",
                    "type": "black",
                    "confidence": 100,
                    "type_weighting": 50,
                    "source": "detection",
                    "entity_message_index": 0
                }
            ]
        )

        self.assertListEqual(
            [
                {
                    'confidence': 100,
                    'entity_message_index': 0,
                    'key': 'color',
                    'source': 'detection',
                    'type': 'black',
                    'type_index_modifier': 1.0,
                    'type_weighting': 50
                }
            ],
            actual
        )

    def test_multiple_entity_different_type_same_message_index(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.create_entity_type_index_modifier(
            [
                {
                    "key": "color",
                    "type": "black",
                    "confidence": 100,
                    "type_weighting": 50,
                    "source": "detection",
                    "entity_message_index": 0
                },
                {
                    "key": "leather",
                    "type": "material",
                    "confidence": 100,
                    "type_weighting": 50,
                    "source": "detection",
                    "entity_message_index": 0
                }
            ]
        )

        self.assertListEqual(
            [
                {
                    'confidence': 100,
                    'entity_message_index': 0,
                    'key': 'color',
                    'source': 'detection',
                    'type': 'black',
                    'type_index_modifier': 1.0,
                    'type_weighting': 50
                },
                {
                    'confidence': 100,
                    'entity_message_index': 0,
                    'key': 'leather',
                    'source': 'detection',
                    'type': 'material',
                    'type_index_modifier': 1.0,
                    'type_weighting': 50
                }
            ],
            actual
        )

    def test_multiple_entity_different_type_different_message_index(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.create_entity_type_index_modifier(
            [
                {
                    "key": "color",
                    "type": "black",
                    "confidence": 100,
                    "type_weighting": 50,
                    "source": "detection",
                    "entity_message_index": 0
                },
                {
                    "key": "leather",
                    "type": "material",
                    "confidence": 100,
                    "type_weighting": 50,
                    "source": "detection",
                    "entity_message_index": 1
                }
            ]
        )

        self.assertListEqual(
            [
                {
                    'confidence': 100,
                    'entity_message_index': 0,
                    'key': 'color',
                    'source': 'detection',
                    'type': 'black',
                    'type_index_modifier': 1.0,
                    'type_weighting': 50
                },
                {
                    'confidence': 100,
                    'entity_message_index': 1,
                    'key': 'leather',
                    'source': 'detection',
                    'type': 'material',
                    'type_index_modifier': 1.0,
                    'type_weighting': 50
                }
            ],
            actual
        )

    def test_multiple_entity_same_type_same_message_index(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.create_entity_type_index_modifier(
            [
                {
                    "key": "color",
                    "type": "black",
                    "confidence": 100,
                    "type_weighting": 50,
                    "source": "detection",
                    "entity_message_index": 0
                },
                {
                    "key": "red",
                    "type": "color",
                    "confidence": 100,
                    "type_weighting": 50,
                    "source": "detection",
                    "entity_message_index": 0
                }
            ]
        )

        self.assertListEqual(
            [
                {
                    'confidence': 100,
                    'entity_message_index': 0,
                    'key': 'color',
                    'source': 'detection',
                    'type': 'black',
                    'type_index_modifier': 1.0,
                    'type_weighting': 50
                },
                {
                    'confidence': 100,
                    'entity_message_index': 0,
                    'key': 'red',
                    'source': 'detection',
                    'type': 'color',
                    'type_index_modifier': 1.0,
                    'type_weighting': 50
                }
            ],
            actual
        )

    def test_multiple_entity_same_type_different_message_index(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.create_entity_type_index_modifier(
            [
                {
                    "type": "color",
                    "key": "black",
                    "confidence": 100,
                    "type_weighting": 50,
                    "source": "detection",
                    "entity_message_index": 0
                },
                {
                    "key": "red",
                    "type": "color",
                    "confidence": 100,
                    "type_weighting": 50,
                    "source": "detection",
                    "entity_message_index": 1
                }
            ]
        )

        self.assertListEqual(
            [
                {
                    'confidence': 100,
                    'entity_message_index': 0,
                    'key': 'black',
                    'source': 'detection',
                    'type': 'color',
                    'type_index_modifier': 0.7071067811865475,
                    'type_weighting': 50
                },
                {
                    'confidence': 100,
                    'entity_message_index': 1,
                    'key': 'red',
                    'source': 'detection',
                    'type': 'color',
                    'type_index_modifier': 1.0,
                    'type_weighting': 50
                }
            ],
            actual
        )


class extract_user_messages(TestCase):
    def test_regular(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        in_messages = target.extract_user_messages(
            [
                {
                    "direction": 1,
                    "_id": 1
                },
                {
                    "direction": 0,
                    "_id": 2
                }
            ]
        )

        self.assertListEqual([{'_id': 1, 'direction': 1}], list(in_messages))


class extract_last_user_message(TestCase):
    def test_items(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        target.extract_user_messages = MagicMock(return_value=["value_1", "value_2"].__iter__())
        actual = target.extract_last_user_message("messages_value")

        self.assertEqual("value_1", actual)


class extract_entities(TestCase):
    def test_none_context(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.extract_entities(None)
        self.assertListEqual([], actual)

    def test_empty_entities(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.extract_entities(
            {
                "entities": []
            }
        )
        self.assertListEqual([], actual)

    def test_entities(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.extract_entities(
            {
                "entities": [
                    "entity_1",
                    "entity_2"
                ]
            }
        )
        self.assertListEqual(
            [
                "entity_1",
                "entity_2"
            ],
            actual
        )


class update_entities(TestCase):
    def test_regular(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        target.add_entity_to_context = MagicMock(
            side_effect=(
                [
                    "context_entities_1"
                ]
            )
        )

        actual = target.update_entities_with_last_message(
            [
                "entity_value"
            ],
            {
                "detection": {
                    "outcomes": [
                        {
                            "intent": "intent_value_1",
                            "entities": [
                                {
                                    "confidence": "confidence_value_1_1",
                                    "type": "type_value_1_1",
                                    "key": "key_value_1_1",
                                    "source": "detection"
                                }
                            ]
                        }
                    ]
                }
            }
        )

        self.assertEqual(1, target.add_entity_to_context.call_count)
        self.assertEqual(['entity_value'], target.add_entity_to_context.call_args_list[0][0][0])
        self.assertEqual('intent_value_1', target.add_entity_to_context.call_args_list[0][0][1])
        self.assertEqual('confidence_value_1_1', target.add_entity_to_context.call_args_list[0][0][2])
        self.assertEqual('type_value_1_1', target.add_entity_to_context.call_args_list[0][0][3])
        self.assertEqual('key_value_1_1', target.add_entity_to_context.call_args_list[0][0][4])

        self.assertEqual("context_entities_1", actual)


class remove_default_entities_if_detections(TestCase):
    def test_no_detections(self):
        context_data = MagicMock()
        context_data.get = MagicMock(return_value="existing_context_value")

        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.remove_default_entities_if_detections(
            [
                {
                    "source": "default",
                    "id": 1
                },
                {
                    "source": "default",
                    "id": 2
                }
            ]
        )

        self.assertListEqual(
            [{'id': 1, 'source': 'default'}, {'id': 2, 'source': 'default'}],
            actual
        )

    def test_some_detections(self):
        context_data = MagicMock()
        context_data.get = MagicMock(return_value="existing_context_value")

        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        actual = target.remove_default_entities_if_detections(
            [
                {
                    "source": "default",
                    "id": 1
                },
                {
                    "source": "default",
                    "id": 2
                },
                {
                    "source": "detection",
                    "id": 1
                }
            ]
        )

        self.assertListEqual(
            [{'id': 1, 'source': 'detection'}],
            actual
        )


class change_entities_weighting(TestCase):
    def test_regular(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        target.calculate_weighting = MagicMock(
            side_effect=[
                31,
                21,
                3
            ]
        )

        actual = target.change_entities_weighting(
            [
                {
                    "id": 1
                },
                {
                    "id": 2
                }
            ]
        )

        self.assertListEqual(
            [{'id': 1, 'weighting': 31}, {'id': 2, 'weighting': 21}],
            actual
        )


class add_product_counts(TestCase):
    def test_regular(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        target.entity_product_count_cache = MagicMock(
            side_effect=(
                100,
                0
            )
        )

        actual = target.add_product_counts(
            [
                {
                    "_id": 1,
                    "key": "black",
                    "type": "color"
                },
                {
                    "_id": 2,
                    "key": "men",
                    "type": "division"
                }
            ]
        )

        self.assertListEqual(
            [
                {
                    'meta': {'instock_product_count': 100}, 'type': 'color', '_id': 1, 'key': 'black'
                },
                {
                    'meta': {'instock_product_count': 0}, 'type': 'division', '_id': 2, 'key': 'men'
                }
            ],
            actual
        )

        self.assertListEqual(
            [
                call('color', 'black'),
                call('division', 'men')
            ],
            target.entity_product_count_cache.call_args_list
        )

class split_unsupported_entities(TestCase):
    def test_regular(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)

        supported, unsupported = target.split_unsupported_entities(
            [
                {
                    "_id": 1,
                    "meta": {
                        "instock_product_count": 0
                    }
                },
                {
                    "_id": 2,
                    "meta": {
                        "instock_product_count": 110
                    }
                }
            ]
        )

        self.assertListEqual(
            [
                {
                    "_id": 2,
                    "meta": {
                        "instock_product_count": 110
                    }
                }
            ],
            supported
        )
        self.assertListEqual(
            [
                {
                    "_id": 1,
                    "meta": {
                        "instock_product_count": 0
                    }
                }
            ],
            unsupported
        )


class update(TestCase):
    def test_last_message_user(self):
        context_data = MagicMock()
        context_data.get = MagicMock(return_value="existing_context_value")
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        target.extract_last_user_message = MagicMock(return_value="last_message")
        target.extract_entities = MagicMock(return_value="extracted_entities")
        target.remove_default_entities_if_detections = MagicMock(return_value="removed_entities")
        target.update_entities_with_last_message = MagicMock(
            return_value="entities_update_entities_with_last_message")
        target.create_entity_type_index_modifier = MagicMock(
            return_value="entities_create_entity_type_index_modifier")
        target.change_entities_weighting = MagicMock(return_value="entities_change_entities_weighting")

        target.add_product_counts = MagicMock(return_value="entities_add_product_counts")
        target.split_unsupported_entities = MagicMock(return_value=("supported_entities", "unsupported_entities"))

        target.update("context_id_value", "_rev_value", "messages_value")

        target.extract_last_user_message.assert_called_once_with("messages_value")
        context_data.get.assert_called_once_with('context_id_value', '_rev_value')
        target.extract_entities.assert_called_once_with('existing_context_value')
        target.update_entities_with_last_message.assert_called_once_with('extracted_entities', 'last_message')
        target.remove_default_entities_if_detections.assert_called_once_with(
            'entities_update_entities_with_last_message')
        target.create_entity_type_index_modifier.assert_called_once_with('removed_entities')
        target.change_entities_weighting.assert_called_once_with('entities_create_entity_type_index_modifier')
        target.add_product_counts.assert_called_once_with('entities_change_entities_weighting')
        target.split_unsupported_entities.assert_called_once_with("entities_add_product_counts")
        context_data.update.assert_called_once_with('context_id_value', '_rev_value', unsupported_entities="unsupported_entities",
                                                    entities='supported_entities')

    def test_last_message_jemboo(self):
        context_data = MagicMock()
        attribute_product_data = MagicMock()

        target = Target(context_data, attribute_product_data)
        target.extract_last_user_message = MagicMock(return_value=None)

        target.update("context_id_value", "_rev_value", "messages_value")

        target.extract_last_user_message.assert_called_once_with("messages_value")
        context_data.update.assert_called_once_with('context_id_value', '_rev_value')

