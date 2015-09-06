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
