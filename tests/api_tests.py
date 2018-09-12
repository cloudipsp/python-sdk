from __future__ import absolute_import, unicode_literals
from cloudipsp import Api, exceptions
from .tests_helper import TestCase


class ApiTest(TestCase):
    def setUp(self):
        self.data = self.get_dummy_data()
        self.api = Api(merchant_id=self.data['merchant']['id'],
                       secret_key=self.data['merchant']['secret'])

    def test_request_type(self):
        api = Api(merchant_id=self.data['merchant']['id'],
                  secret_key=self.data['merchant']['secret'],
                  request_type='xml')
        self.assertEqual(api.request_type, 'xml')

    def test_api_domain(self):
        api = Api(merchant_id=self.data['merchant']['id'],
                  secret_key=self.data['merchant']['secret'],
                  api_domain='api.test.eu')
        self.assertEqual(api.api_url, 'https://api.test.eu/api')

    def test_api_protocol(self):
        api = Api(merchant_id=self.data['merchant']['id'],
                  secret_key=self.data['merchant']['secret'],
                  api_protocol='2.0')
        self.assertEqual(api.api_protocol, '2.0')

    def test_api_except(self):
        with self.assertRaises(ValueError):
            Api(merchant_id=self.data['merchant']['id'],
                secret_key=self.data['merchant']['secret'],
                api_protocol='2.0',
                request_type='xml'
                )

    def test_post(self):
        with self.assertRaises(exceptions.ServiceError):
            self.api._request(self.api.api_url,
                              method="POST",
                              data=None,
                              headers=None)

    def test_headers(self):
        self.assertEqual(self.api._headers().get('User-Agent'),
                         'Python SDK')
        self.assertEqual(self.api._headers().get('Content-Type'),
                         'application/json; charset=utf-8')
