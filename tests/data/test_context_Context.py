from bson import ObjectId

__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from context.data.context import Context as Target, MessageDirection
from datetime import datetime


class get_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.collection.find.return_value = ["first", "second"]
        actual = target.get("_id_value")

        self.assertEqual("first", actual)

        self.assertEqual(1, target.collection.find.call_count)
        self.assertDictEqual(
            {'_id': '_id_value'},
            target.collection.find.call_args_list[0][0][0]
        )


class insert_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        actual = target.insert(
            "entities_value",
            "locale_value",
            "new_context_id_value",
            "application_id_value",
            "session_id",
            "user_id",
            "detection_id_value",
            datetime(2000, 1, 1)
        )

        self.assertDictEqual(
            {'_ver': 'new_context_id_value', '_id': 'new_context_id_value'},
            actual
        )

        self.assertEqual(1, target.collection.insert.call_count)
        self.assertDictEqual(
            {
                '_id': 'new_context_id_value',
                'created': '2000-01-01T00:00:00',
                'detection_id': 'detection_id_value',
                'entities': 'entities_value',
                'locale': 'locale_value',
                'session_id': 'session_id',
                'application_id': 'application_id_value',
                'user_id': 'user_id',
                '_ver': 'new_context_id_value',
                'version': "0.0.2"
            },
            target.collection.insert.call_args_list[0][0][0]
        )

    def test_none_user_id(self):
        target = Target()
        target.collection = Mock()
        actual = target.insert(
            "entities_value",
            "locale_value",
            "new_context_id_value",
            "application_id_value",
            "session_id",
            None,
            "detection_id_value",
            datetime(2000, 1, 1)
        )

        self.assertDictEqual(
            {'_ver': 'new_context_id_value', '_id': 'new_context_id_value'},
            actual
        )

        self.assertEqual(1, target.collection.insert.call_count)
        self.assertDictEqual(
            {
                '_id': 'new_context_id_value',
                'created': '2000-01-01T00:00:00',
                'entities': 'entities_value',
                'locale': 'locale_value',
                'session_id': 'session_id',
                'application_id': 'application_id_value',
                'detection_id': 'detection_id_value',
                '_ver': 'new_context_id_value',
                'version': '0.0.2'
            },
            target.collection.insert.call_args_list[0][0][0]
        )

    def test_none_detection_id(self):
        target = Target()
        target.collection = Mock()
        actual = target.insert(
            "entities_value",
            "locale_value",
            "new_context_id_value",
            "application_id_value",
            "session_id",
            "user_id",
            None,
            datetime(2000, 1, 1)
        )

        self.assertDictEqual(
            {'_ver': 'new_context_id_value', '_id': 'new_context_id_value'},
            actual
        )

        self.assertEqual(1, target.collection.insert.call_count)
        self.assertDictEqual(
            {
                '_id': 'new_context_id_value',
                'created': '2000-01-01T00:00:00',
                'entities': 'entities_value',
                'locale': 'locale_value',
                'session_id': 'session_id',
                'application_id': 'application_id_value',
                'user_id': 'user_id',
                '_ver': 'new_context_id_value',
                'version': '0.0.2'
            },
            target.collection.insert.call_args_list[0][0][0]
        )


class get_messages_tests(TestCase):
    def test_messages(self):
        target = Target()
        target.collection = Mock()
        target.collection.find.return_value = [{
                    "messages": "messages_value"
                }, "second"]
        actual = target.find_messages(ObjectId("012345678901234567890123"))

        self.assertEqual(
            "messages_value",
            actual
        )

        self.assertEqual(1, target.collection.find.call_count)
        self.assertDictEqual(
            {'_id': ObjectId('012345678901234567890123')},
            target.collection.find.call_args_list[0][0][0]
        )
        self.assertDictEqual(
            {'messages': 1},
            target.collection.find.call_args_list[0][0][1]
        )

    def test_no_messages(self):
        target = Target()
        target.collection = Mock()
        target.collection.find.return_value = ["first", "second"]
        actual = target.find_messages(ObjectId("012345678901234567890123"))

        self.assertListEqual([], actual)

        self.assertEqual(1, target.collection.find.call_count)
        self.assertDictEqual(
            {'_id': ObjectId('012345678901234567890123')},
            target.collection.find.call_args_list[0][0][0]
        )
        self.assertDictEqual(
            {'messages': 1},
            target.collection.find.call_args_list[0][0][1]
        )


class insert_message_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        actual = target.insert_message(
            ObjectId("012345678901234567890123"),
            MessageDirection.IN,
            "text_value",
            now=datetime(2000, 1, 1),
            _id=ObjectId('992345678901234567890123')
        )

        self.assertEqual(1, target.collection.update.call_count)
        self.assertDictEqual(
            {
                '_id': ObjectId('012345678901234567890123')
            },
            target.collection.update.call_args_list[0][0][0]
        )
        self.assertDictEqual(
            {
                '$push': {
                    'messages': {
                        '_id': ObjectId('992345678901234567890123'),
                        'updated': '2000-01-01T00:00:00',
                        'created': '2000-01-01T00:00:00',
                        'text': 'text_value',
                        'direction': 1,
                        'version': "0.0.2"
                    }
                }
            },
            target.collection.update.call_args_list[0][0][1]
        )

        self.assertEqual(
            ObjectId('992345678901234567890123'),
            actual
        )

    def test_with_detection_id(self):
        target = Target()
        target.collection = Mock()
        actual = target.insert_message(
            ObjectId("012345678901234567890123"),
            MessageDirection.IN,
            "text_value",
            detection_id=ObjectId("A12345678901234567890123"),
            now=datetime(2000, 1, 1),
            _id=ObjectId('992345678901234567890123')
        )

        self.assertEqual(1, target.collection.update.call_count)

        self.assertDictEqual(
            {
                '_id': ObjectId('012345678901234567890123')
            },
            target.collection.update.call_args_list[0][0][0]
        )
        self.assertDictEqual(
            {
                '$push': {
                    'messages': {
                        '_id': ObjectId('992345678901234567890123'),
                        'detection_id': ObjectId('a12345678901234567890123'),
                        'updated': '2000-01-01T00:00:00',
                        'created': '2000-01-01T00:00:00',
                        'text': 'text_value',
                        'direction': 1,
                        'version': "0.0.2"
                    }
                }
            },
            target.collection.update.call_args_list[0][0][1]
        )

        self.assertEqual(
            ObjectId('992345678901234567890123'),
            actual
        )
