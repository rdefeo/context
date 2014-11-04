__author__ = 'robdefeo'
import unittest

from mock import Mock
from context.data.interest import Interest as Target
from datetime import datetime


class upsert_tests(unittest.TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()

        target.upsert("product_id_value", "user_id_value", True, "heart", "date_value")

        self.assertEquals(target.collection.update.call_count, 1)
        self.assertDictEqual(
            target.collection.update.call_args_list[0][0][0],
            {
                'type': 'heart',
                'user_id': 'user_id_value',
                'product_id': 'product_id_value'
            }
        )
        self.assertDictEqual(
            target.collection.update.call_args_list[0][0][1],
            {
                '$set': {
                    'active': True,
                    'updated': 'date_value'
                },
                '$setOnInsert': {
                    'created': 'date_value',
                    'product_id': 'product_id_value',
                    'type': 'heart',
                    'user_id': 'user_id_value'
                }
            }
        )

