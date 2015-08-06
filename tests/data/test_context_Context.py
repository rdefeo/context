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
        target.insert(
            "entities_value",
            "locale_value",
            "new_context_id_value",
            "application_id_value",
            "session_id",
            "user_id",
            "detection_id_value",
            datetime(2000, 1, 1)
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
                'version': "0.0.2"
            },
            target.collection.insert.call_args_list[0][0][0]
        )

    def test_none_user_id(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            "entities_value",
            "locale_value",
            "new_context_id_value",
            "application_id_value",
            "session_id",
            None,
            "detection_id_value",
            datetime(2000, 1, 1)
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
                'version': '0.0.2'
            },
            target.collection.insert.call_args_list[0][0][0]
        )

    def test_none_detection_id(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            "entities_value",
            "locale_value",
            "new_context_id_value",
            "application_id_value",
            "session_id",
            "user_id",
            None,
            datetime(2000, 1, 1)
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
                'version': '0.0.2'
            },
            target.collection.insert.call_args_list[0][0][0]
        )