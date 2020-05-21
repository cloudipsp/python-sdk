from __future__ import absolute_import, unicode_literals
from cloudipsp.resources import Resource
from datetime import datetime

import cloudipsp.helpers as helper


class Checkout(Resource):
    def url(self, data):
        """
        Method to generate checkout url
        :param data: order data
        :return: api response
        """
        path = '/checkout/url/'
        params = self._required(data)
        result = self.api.post(path, data=params, headers=self.__headers__)

        return self.response(result)

    def token(self, data):
        """
        Method to generate checkout token
        :param data: order data
        :return: api response
        """
        path = '/checkout/token/'
        params = self._required(data)
        result = self.api.post(path, data=params, headers=self.__headers__)

        return self.response(result)

    def verification(self, data):
        """
        Method to generate checkout verification url
        :param data: order data
        :return: api response
        """
        path = '/checkout/url/'
        verification_data = {
            'verification': 'Y',
            'verification_type': data.get('verification_type', 'code')
        }
        data.update(verification_data)
        params = self._required(data)
        result = self.api.post(path, data=params, headers=self.__headers__)

        return self.response(result)

    def subscription(self, data):
        """
        Method to generate checkout url with calendar
        :param data: order data
        :return: api response
        """
        if self.api.api_protocol != '2.0':
            raise Exception('This method allowed only for v2.0')
        path = '/checkout/url/'
        recurring_data = data.get('recurring_data', '')
        subscription_data = {
            'subscription': 'Y',
            'recurring_data': {
                'start_time': recurring_data.get('start_time', ''),
                'amount': recurring_data.get('amount', ''),
                'every': recurring_data.get('every', ''),
                'period': recurring_data.get('period', ''),
                'readonly': recurring_data.get('readonly', ''),
            }
        }

        helper.check_data(subscription_data['recurring_data'])
        self._validate_recurring_data(subscription_data['recurring_data'])
        subscription_data.update(data)
        params = self._required(subscription_data)
        result = self.api.post(path, data=params, headers=self.__headers__)

        return self.response(result)

    @staticmethod
    def _validate_recurring_data(data):
        """
        Validation recurring data params
        :param data: recurring data
        :return: exception
        """
        try:
            datetime.strptime(data['start_time'], '%Y-%m-%d')
        except ValueError:
            raise ValueError(
                "Incorrect date format. 'Y-m-d' is allowed")
        if data['period'] not in ('day', 'week', 'month'):
            raise ValueError(
                "Incorrect period. ('day','week','month') is allowed")

    def _required(self, data):
        """
        Required data to send
        :param data:
        :return: parameters to send
        """
        self.order_id = data.get('order_id') or helper.generate_order_id()
        order_desc = data.get('order_desc') or helper.get_desc(self.order_id)
        params = {
            'order_id': self.order_id,
            'order_desc': order_desc,
            'amount': data.get('amount', ''),
            'currency': data.get('currency', '')
        }
        helper.check_data(params)
        params.update(data)

        return params
