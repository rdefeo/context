from bson import ObjectId

__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from context.data.context import Context as Target
from datetime import datetime


class get_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.collection.find.return_value = ["first", "second"]
        actual = target.get("_id_value", "_ver_value")

        self.assertEqual("first", actual)

        self.assertEqual(1, target.collection.find.call_count)
        self.assertDictEqual(
            {'_id': '_id_value'},
            target.collection.find.call_args_list[0][0][0]
        )

class update_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        actual = target.update(
            "context_id_value",
            "new_ver_id_value",
            datetime(2000, 1, 1)
        )

        self.assertEqual(
            "new_ver_id_value",
            actual
        )

        self.assertEqual(1, target.collection.update.call_count)
        self.assertDictEqual(
            {
                '_id': 'context_id_value'
            },
            target.collection.update.call_args_list[0][0][0]
        )
        self.assertDictEqual(
            {
                '$set': {
                    '_ver': 'new_ver_id_value',
                    'updated': '2000-01-01T00:00:00'
                }
            },
            target.collection.update.call_args_list[0][0][1]
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
                '_ver': 'new_context_id_value',
                'version': '0.0.2'
            },
            target.collection.insert.call_args_list[0][0][0]
        )
