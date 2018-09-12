from __future__ import absolute_import, unicode_literals


class RequestError(Exception):
    """
    Some required param is missing.
    """

    def __init__(self, param):
        self.param = param

    def __str__(self):
        return "Required parameter '%s' is missing." % self.param


class ResponseError(Exception):
    """
    Handling api response error.
    """

    def __init__(self, response):
        self.response = response

    def __str__(self):
        message = ''
        if 'response_status' in self.response:
            message += "Response status is %s." \
                       % self.response.get('response_status', '')
        if 'error_message' in self.response:
            message += " Error message: %s." \
                       % (self.response.get('error_message'))
        if 'error_code' in self.response:
            message += " Error code: %s." \
                       % (self.response.get('error_code'))
        if 'request_id' in self.response:
            message += " Request id: %s." \
                       % (self.response.get('request_id'))
        message += " Check parameters"
        return message


class ServiceError(Exception):
    """
    If response code not in (200, 201).
    """
