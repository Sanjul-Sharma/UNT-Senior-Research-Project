"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""
import json
from json import JSONDecodeError
from urllib.parse import urlencode

import requests

from settings import SITE_ROOT

__author__ = "Sanjul Sharma"


class RequestProcessor(object):
    api_url = None
    headers = {}

    def __init__(self, **kwargs):
        self.api_url = "{base_url}{path}".format(base_url=SITE_ROOT, path=kwargs.get("path"))
        self.headers = {"content-type": "application/json"}

    def get_data(self, params=None, verify=True):
        """
        :param params: params can have extra parameters like,
                       https://example.com/api/v1/users/?page_size=2&format=json
                       In this case params will be look like, {'page_size': 2, 'format': 'json'}
        :param verify: (True) will only allow true https clients
        :return: api response
        """
        if self.api_url is None:
            raise Exception('URL can not be UNDEFINED')

        response = requests.get(
            self.api_url, params=params, headers=self.headers, verify=verify, timeout=180
        )
        try:
            return json.loads(response.text)
        except JSONDecodeError:
            # if returns 404, 403 or something else (ERROR)
            return response.status_code

    def post_data(self, body=None, verify=True):
        """
        :param body: post body format dictionary object or JSON
        :param verify: (True) will only allow true https clients
        :return: api response
        """
        if self.api_url is None:
            raise Exception('URL can not be UNDEFINED')
        if body is None:
            raise Exception('BODY can not be UNDEFINED')
        if self.headers['content-type'] == 'application/x-www-form-urlencoded':
            body = urlencode(body).encode()
        elif self.headers['content-type'] == 'application/json':
            body = json.dumps(body)
        response = requests.post(
            self.api_url, data=body, headers=self.headers, verify=verify, timeout=60
        )
        try:
            return json.loads(response.text)
        except JSONDecodeError:
            # if returns 404, 403 or something else (ERROR)
            return response.status_code
