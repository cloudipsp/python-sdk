from __future__ import absolute_import, unicode_literals

import json
from cloudipsp import Order
from .tests_helper import TestCase


class OrderTest(TestCase):
    def setUp(self):
        self.api = self.get_api()
        self.order = Order(api=self.api)
        self.order_id = self.create_order().get('order_id')

    def test_get_order_status(self):
        data = {
            'order_id': self.order_id
        }
        response = self.order.status(data)
        self.assertEqual(response.get('response_status'), 'success')
        self.assertIn('order_status', response)

    def test_get_order_trans_list(self):
        data = {
            'order_id': self.order_id
        }
        response = self.order.transaction_list(data)
        self.assertIsInstance(response, list)
        self.assertIn('order_id', response[0])

    def test_refund(self):
        data = {
            'order_id': self.order_id
        }
        data.update(self.data['order_full_data'])
        response = self.order.reverse(data)
        self.assertEqual(response.get('response_status'), 'success')
        self.assertIn('reverse_status', response)

    def test_capture(self):
        data = {
            'order_id': self.order_id
        }
        data.update(self.data['order_full_data'])
        response = self.order.capture(data)
        self.assertEqual(response.get('response_status'), 'success')
        self.assertEqual(response.get('order_id'), self.order_id)
        self.assertEqual(response.get('capture_status'), 'captured')

    def test_settlement(self):
        self.api.api_protocol = '2.0'
        data = {
            'operation_id': self.order_id,
            'receiver': [
                {
                    'requisites': {
                        'amount': 500,
                        'merchant_id': 600001
                    },
                    'type': 'merchant'
                },
                {
                    'requisites': {
                        'amount': 500,
                        'merchant_id': 700001
                    },
                    'type': 'merchant'
                }
            ]
        }
        data.update(self.data['order_full_data'])
        data_capture = {
            'order_id': self.order_id
        }
        data_capture.update(self.data['order_full_data'])
        self.order.capture(data_capture)
        response = self.order.settlement(data)
        response_data = json.loads(response.get('data'))
        self.assertEqual(response_data.get('order')['order_status'], 'created')
        self.assertIn('payment_id', response_data.get('order'))
