from bson import ObjectId

__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from context.data.message import Direction, Message as Target
from datetime import datetime


class get_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.collection.find.return_value = ["first", "second"]
        actual = target.find(ObjectId("012345678901234567890123"))

        self.assertListEqual(['first', 'second'], actual)

        self.assertEqual(1, target.collection.find.call_count)
        self.assertDictEqual(
            {'context_id': ObjectId('012345678901234567890123')},
            target.collection.find.call_args_list[0][0][0]
        )


class update_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.update(
            ObjectId("012345678901234567890123"),
            now=datetime(2000, 1, 1)
        )

        self.assertEqual(1, target.collection.update.call_count)
        self.assertDictEqual(
            {
                '_id': ObjectId('012345678901234567890123')
            },
            target.collection.update.call_args_list[0][0][0]
        )
        self.assertDictEqual(
            {'$set': {'updated': '2000-01-01T00:00:00'}},
            target.collection.update.call_args_list[0][0][1],

        )


class insert_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            ObjectId("012345678901234567890123"),
            Direction.IN,
            "text_value",
            now=datetime(2000, 1, 1)
        )

        self.assertEqual(1, target.collection.insert.call_count)
        self.assertDictEqual(
            {
                'context_id': ObjectId('012345678901234567890123'),
                'updated': '2000-01-01T00:00:00',
                'created': '2000-01-01T00:00:00',
                'text': 'text_value',
                'direction': 1,
                'version': "0.0.2"
            },
            target.collection.insert.call_args_list[0][0][0]
        )

    def test_with_detection_id(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            ObjectId("012345678901234567890123"),
            Direction.IN,
            "text_value",
            detection_id=ObjectId("A12345678901234567890123"),
            now=datetime(2000, 1, 1)
        )

        self.assertEqual(1, target.collection.insert.call_count)

        self.assertDictEqual(
            {
                'context_id': ObjectId('012345678901234567890123'),
                'detection_id': ObjectId('a12345678901234567890123'),
                'updated': '2000-01-01T00:00:00',
                'created': '2000-01-01T00:00:00',
                'text': 'text_value',
                'direction': 1,
                'version': "0.0.2"
            },
            target.collection.insert.call_args_list[0][0][0]
        )
