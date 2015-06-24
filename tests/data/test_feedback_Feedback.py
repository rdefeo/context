__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from context.data.feedback import Feedback as Target
from datetime import datetime


class insert_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            "user_id",
            "application_id_value",
            "session_id",
            "context_id",
            "product_id",
            "action_type",
            "meta_data_value",
            datetime(2000, 1, 1)
        )

        self.assertEqual(
            target.collection.insert.call_count,
            1
        )
        self.assertDictEqual(
            target.collection.insert.call_args_list[0][0][0],
            {
                'created': '2000-01-01T00:00:00',
                'type': 'action_type',
                'context_id': 'context_id',
                'product_id': 'product_id',
                'session_id': 'session_id',
                'application_id': 'application_id_value',
                'user_id': 'user_id',
                'meta_data': 'meta_data_value',
                'version': '0.0.2'
            }
        )

    def test_none_meta_data(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            None,
            "application_id_value",
            "session_id",
            "context_id",
            "product_id",
            "action_type",
            "meta_data_value",
            datetime(2000, 1, 1)
        )

        self.assertEqual(
            target.collection.insert.call_count,
            1
        )
        self.assertDictEqual(
            target.collection.insert.call_args_list[0][0][0],
            {
                'created': '2000-01-01T00:00:00',
                'type': 'action_type',
                'context_id': 'context_id',
                'product_id': 'product_id',
                'session_id': 'session_id',
                'application_id': 'application_id_value',
                'meta_data': 'meta_data_value',
                'version': '0.0.2'
            }
        )

    def test_none_user_id(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            "user_id",
            "application_id_value",
            "session_id",
            "context_id",
            "product_id",
            "action_type",
            None,
            datetime(2000, 1, 1)
        )

        self.assertEqual(
            target.collection.insert.call_count,
            1
        )
        self.assertDictEqual(
            target.collection.insert.call_args_list[0][0][0],
            {
                'created': '2000-01-01T00:00:00',
                'type': 'action_type',
                'context_id': 'context_id',
                'product_id': 'product_id',
                'session_id': 'session_id',
                'application_id': 'application_id_value',
                'user_id': 'user_id',
                'version': '0.0.2'
            }
        )

    def test_none_context_id(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            "user_id",
            "application_id_value",
            "session_id",
            None,
            "product_id",
            "action_type",
            "meta_data_value",
            datetime(2000, 1, 1)
        )

        self.assertEqual(
            target.collection.insert.call_count,
            1
        )
        self.assertDictEqual(
            target.collection.insert.call_args_list[0][0][0],
            {
                'created': '2000-01-01T00:00:00',
                'type': 'action_type',
                'product_id': 'product_id',
                'session_id': 'session_id',
                'application_id': 'application_id_value',
                'user_id': 'user_id',
                'version': '0.0.2',
                'meta_data': 'meta_data_value'
            }
        )