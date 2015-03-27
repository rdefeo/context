__author__ = 'robdefeo'
from unittest import TestCase
from mock import Mock
from context.data.context import Context as Target
from datetime import datetime


class insert_tests(TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.insert(
            "entities_value",
            "locale_value",
            "new_context_id_value",
            "session_id",
            "user_id",
            "detection_id_value",
            datetime(2000, 1, 1)
        )

        self.assertEqual(
            target.collection.insert.call_count,
            1
        )
        self.assertDictEqual(
            target.collection.insert.call_args_list[0][0][0],
            {
                '_id': 'new_context_id_value',
                'created': '2000-01-01T00:00:00',
                'detection_id': 'detection_id_value',
                'entities': 'entities_value',
                'locale': 'locale_value',
                'session_id': 'session_id',
                'user_id': 'user_id'
            }
        )