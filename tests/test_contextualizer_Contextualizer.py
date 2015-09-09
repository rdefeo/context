from bson import ObjectId

__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from context.contextualizer import Contextualizer as Target
from datetime import datetime


class add_entity_to_context_tests(TestCase):
    def test_empty_entities(self):
        target = Target(Mock())
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
        target = Target(Mock())
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
        target = Target(Mock())
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
        target = Target(Mock())
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
        target = Target(Mock())
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
        target = Target(Mock())
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
        target = Target(Mock())
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
        target = Target(Mock())
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
        context_data = Mock()
        target = Target(context_data)
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

    