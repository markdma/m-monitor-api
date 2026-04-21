# coding=utf8

import requests
import json as j


class HttpHelper:

    def __init__(self, url, timeout=10, header=None):
        self.url = url
        self.timeout = timeout
        self.header = header

    def http_get(self, params=None, decode_json=None, json=None, params2=None):
        """

        :param params:
        :param decode_json:
        :param json:
        :param params2:
        :return:
        """
        ret = requests.get(
            self.url,
            data=params,
            timeout=self.timeout,
            json=json,
            params=params2,
            headers=self.header)
        if decode_json:
            return j.loads(ret.content)
        return ret

    def http_post(self, params=None, decode_json=None, headers=None, json_data=None):
        """

        :param params:
        :param decode_json:
        :param headers:
        :param json_data:
        :return:
        """
        if not headers:
            headers = self.header
        ret = requests.post(
            self.url,
            params,
            timeout=self.timeout,
            headers=headers,
            json=json_data)
        if decode_json:
            return j.loads(ret.content)
        return ret
