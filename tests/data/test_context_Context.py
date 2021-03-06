__author__ = 'robdefeo'
from unittest import TestCase
from datetime import datetime

from mock import Mock

from context.data.context import Context as Target


class get_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.collection.find.return_value = ["first", "second"].__iter__()
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
            "entites_value",
            now=datetime(2000, 1, 1)
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
                    '_rev': 'new_ver_id_value',
                    'entities': 'entites_value',
                    'updated': '2000-01-01T00:00:00',
                    'unsupported_entities': {}
                }
            },
            target.collection.update.call_args_list[0][0][1]
        )

    def test_entities_none(self):
        target = Target()
        target.collection = Mock()
        actual = target.update(
            "context_id_value",
            "new_ver_id_value",
            entities=None,
            now=datetime(2000, 1, 1)
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
                    '_rev': 'new_ver_id_value',
                    'updated': '2000-01-01T00:00:00',
                    'unsupported_entities': {}
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
            {'_rev': 'new_context_id_value', '_id': 'new_context_id_value'},
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
                '_rev': 'new_context_id_value',
                'version': "0.0.3"
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
            {'_rev': 'new_context_id_value', '_id': 'new_context_id_value'},
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
                '_rev': 'new_context_id_value',
                'version': '0.0.3'
            },
            target.collection.insert.call_args_list[0][0][0]
        )
