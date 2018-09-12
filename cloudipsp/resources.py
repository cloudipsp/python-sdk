from __future__ import absolute_import, unicode_literals
from cloudipsp import utils
from cloudipsp import exceptions


class Resource(object):
    def __init__(self, api=None, headers=None):
        self.__dict__['api'] = api

        super(Resource, self).__setattr__('__data__', {})
        super(Resource, self).__setattr__('__headers__', headers or {})
        super(Resource, self).__setattr__('order_id', None)

    def __str__(self):
        return self.__data__.__str__()

    def __repr__(self):
        return self.__data__.__str__()

    def __getattr__(self, name):
        try:
            return self.__data__[name]
        except KeyError:
            return super(Resource, self).__getattribute__(name)

    def __setattr__(self, name, value):
        try:
            super(Resource, self).__setattr__(name, value)
        except AttributeError:
            self.__data__[name] = self.convert(name, value)

    def __contains__(self, name):
        return name in self.__data__

    def get_url(self):
        if 'checkout_url' in self.__data__:
            return self.__getattr__('checkout_url')

    def response(self, response):
        """
        :param response: api response
        :return: result
        """
        try:
            result = None
            if self.api.request_type == 'json':
                result = utils.from_json(response).get('response', '')
            if self.api.request_type == 'xml':
                result = utils.from_xml(response).get('response', '')
            if self.api.request_type == 'form':
                result = utils.from_form(response)
            return self._get_result(result)
        except KeyError:
            raise ValueError('Undefined format error.')

    def _get_result(self, result):
        """
        in some api param response_status not exist...
        :param result: api result
        :return: exception
        """
        if 'error_message' in result:
            raise exceptions.ResponseError(result)
        if 'data' in result and self.api.api_protocol == '2.0':
            result['data'] = utils.from_b64(result['data'])
        self.__data__ = result
        return result
