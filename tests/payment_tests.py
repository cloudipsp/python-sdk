from __future__ import absolute_import, unicode_literals
from cloudipsp import Api, Payment, Pcidss
from .tests_helper import TestCase
from datetime import datetime, timedelta


class PaymentTest(TestCase):
    def setUp(self):
        self.api = self.get_api()
        self.payment = Payment(api=self.api)
        self.pcidss = Pcidss(api=self.api)

    def test_recurring_payment(self):
        token = self.create_order().get('rectoken')
        data = {
            "rectoken": token
        }
        data.update(self.data['checkout_data'])
        response = self.payment.recurring(data)
        self.assertEqual(response.get('response_status'), 'success')
        self.assertIn('order_status', response)
        self.assertEqual(response.get('order_status'), 'approved')

    def test_reports(self):
        data = {
            "date_from": (datetime.now() - timedelta(minutes=240)).strftime('%d.%m.%Y %H:%M:%S'),
            "date_to": datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        }
        response = self.payment.reports(data)
        self.assertIsInstance(response, list)

    def test_p2pcredit(self):
        api = Api(merchant_id=1000, secret_key='testcredit')
        payment = Payment(api=api)
        response = payment.p2pcredit(self.data['payment_p2p'])
        self.assertEqual(response.get('response_status'), 'success')
        self.assertIn('order_status', response)

    def test_non3dpcidss_step_one(self):
        data = self.data['payment_pcidss_non3ds']
        response = self.pcidss.step_one(data)
        self.assertEqual(response.get('response_status'), 'success')
        self.assertIn('order_status', response)
        self.assertEqual(response.get('order_status'), 'approved')

    def test_3dspcidss_step_one(self):
        data = self.data['payment_pcidss_3ds']
        response = self.pcidss.step_one(data)
        self.assertEqual(response.get('response_status'), 'success')
        self.assertIn('acs_url', response)
        self.assertIn('pareq', response)
