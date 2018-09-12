from __future__ import absolute_import, unicode_literals
from cloudipsp import utils
from .tests_helper import TestCase


class UtilTest(TestCase):
    def setUp(self):
        self.data = self.get_dummy_data()

    def test_to_xml(self):
        xml = utils.to_xml(self.data['checkout_data'])
        self.assertEqual(xml, '<?xml version="1.0" encoding="UTF-8"?><amount>100</amount><currency>USD</currency>')

    def test_from_xml(self):
        xml = utils.to_xml({'req': self.data['checkout_data']})
        json = utils.from_xml(xml)
        self.assertEqual(json, {'req': self.data['checkout_data']})

    def test_to_form(self):
        form = utils.to_form(self.data['checkout_data'])
        self.assertEqual(form, 'amount=100&currency=USD')

    def test_from_from(self):
        form = utils.to_form(self.data['checkout_data'])
        json = utils.from_form(form)
        self.assertEqual(json, self.data['checkout_data'])

    def test_join_url(self):
        join_url = utils.join_url("checkout", "order")
        self.assertEqual(join_url, "checkout/order")
        join_url = utils.join_url("order/", "3ds")
        self.assertEqual(join_url, "order/3ds")
