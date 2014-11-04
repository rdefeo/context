from bson import ObjectId

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

class find_type_Tests(unittest.TestCase):
    def test_regular(self):
        target = Target()
        target.collection = Mock()
        target.collection.find.return_value = [
            {
                "_id": ObjectId("54595685d3836b8a71241fc4"),
                "active": True,
                "created": "2014-11-04T22:43:17.896800",
                "product_id": "product_id_value_1",
                "type": "heart",
                "updated": "2014-11-04T22:43:21.447936",
                "user_id": "user_id_value"
            },
            {
                "_id": ObjectId("54595685d3836b8a71241fc4"),
                "active": True,
                "created": "2014-11-04T22:43:17.896800",
                "product_id": "product_id_value_2",
                "type": "heart",
                "updated": "2014-11-04T22:43:21.447936",
                "user_id": "user_id_value"
            }
        ]
        actual = target.find("user_id_value", "type_value")

        self.assertEquals(
            target.collection.find.call_count, 1)
        self.assertDictEqual(
            target.collection.find.call_args_list[0][0][0],
            {'active': True, 'type': 'type_value', 'user_id': 'user_id_value'}
        )

        self.assertListEqual(
            actual,
            [
                {
                    'product_id': 'product_id_value_1',
                    'type': 'heart'
                },
                {
                    'product_id': 'product_id_value_2',
                    'type': 'heart'
                }
            ]
        )