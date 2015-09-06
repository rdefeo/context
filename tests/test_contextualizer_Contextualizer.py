from bson import ObjectId

__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from context.contextualizer import Contextualizer as Target
from datetime import datetime


class create_tests(TestCase):
    def test_regular(self):
        context_data = Mock()
        target = Target(context_data)
        target.create("context_id_value", "user_id_value", "application_id_value", "session_id_value", "locale_value")

        self.assertEqual(1, context_data.insert.call_count)
        self.assertListEqual(
            [
                {'type': 'popular', 'key': 'popular', 'source': 'default', 'weighting': 30.0, 'type_weighting': 30.0},
                {'type': 'added', 'key': 'added', 'source': 'default', 'weighting': 30.0, 'type_weighting': 30.0}
            ]
            , context_data.insert.call_args_list[0][0][0])
        self.assertEqual("locale_value", context_data.insert.call_args_list[0][0][1])
        self.assertEqual("context_id_value", context_data.insert.call_args_list[0][0][2])
        self.assertEqual("application_id_value", context_data.insert.call_args_list[0][0][3])
        self.assertEqual("session_id_value", context_data.insert.call_args_list[0][0][4])
        self.assertEqual("user_id_value", context_data.insert.call_args_list[0][0][5])


class create_entity_type_index_modifier_tests(TestCase):
    def test_empty_entities(self):
        target = Target(None)
        actual = target.create_entity_type_index_modifier([])

        self.assertListEqual(
            [],
            actual
        )

    def test_single_entity(self):
        target = Target(None)
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
        target = Target(None)
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
        target = Target(None)
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
        target = Target(None)
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
        target = Target(None)
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

    