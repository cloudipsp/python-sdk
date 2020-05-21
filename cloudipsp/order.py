from __future__ import absolute_import, unicode_literals
from cloudipsp.resources import Resource

import cloudipsp.utils as utils
import cloudipsp.helpers as helper


class Order(Resource):
    def settlement(self, data):
        """
        Method for create split order
        :param data: split order data
        :return: api response
        """
        if self.api.api_protocol != '2.0':
            raise Exception('This method allowed only for v2.0')
        path = '/settlement/'
        params = {
            'order_type': data.get('order_type', 'settlement'),
            'order_id': data.get('order_id') or helper.generate_order_id(),
            'operation_id': data.get('operation_id', ''),
            'receiver': data.get('receiver', [])
        }
        helper.check_data(params)
        params.update(data)
        result = self.api.post(path, data=params, headers=self.__headers__)

        return self.response(result)

    def capture(self, data):
        """
        Method for capturing order
        :param data: capture order data
        :return: api response
        """
        path = '/capture/order_id/'
        params = {
            'order_id': data.get('order_id', ''),
            'amount': data.get('amount', ''),
            'currency': data.get('currency', '')
        }
        helper.check_data(params)
        params.update(data)
        result = self.api.post(path, data=params, headers=self.__headers__)
        return self.response(result)

    def reverse(self, data):
        """
        Method to reverse order
        :param data: reverse order data
        :return: api response
        """
        path = '/reverse/order_id/'
        params = {
            'order_id': data.get('order_id', ''),
            'amount': data.get('amount', ''),
            'currency': data.get('currency', '')
        }
        helper.check_data(params)
        params.update(data)
        result = self.api.post(path, data=params, headers=self.__headers__)
        return self.response(result)

    def status(self, data):
        """
        Method for checking order status
        :param data: order data
        :return: api response
        """
        path = '/status/order_id/'
        params = {
            'order_id': data.get('order_id', '')
        }
        helper.check_data(params)
        params.update(data)
        result = self.api.post(path, data=params, headers=self.__headers__)
        return self.response(result)

    def transaction_list(self, data):
        """
        Method for getting order transaction list
        :param data: order data
        :return: api response
        """
        path = '/transaction_list/'
        params = {
            'order_id': data.get('order_id', '')
        }
        helper.check_data(params)
        params.update(data)
        """
        only json allowed all other methods returns 500 error
        """
        self.api.request_type = 'json'
        result = self.api.post(path, data=params, headers=self.__headers__)
        return self.response(result)

    def atol_logs(self, data):
        """
        Method for getting order atol logs
        :param data: order data
        :return: api response
        """
        path = '/get_atol_logs/'
        params = {
            'order_id': data.get('order_id', '')
        }
        helper.check_data(params)
        params.update(data)
        result = self.api.post(path, data=params, headers=self.__headers__)
        return utils.from_json(result).get('response')
