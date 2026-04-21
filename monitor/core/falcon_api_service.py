# coding=utf8
import copy

from monitor.core.http_helper import HttpHelper
from monitor.core import config
import json as j


class FalconApiService(object):
    """
    调用falcon-api服务
    """

    def __init__(self):
        self.falcon_api_config = self._get_falcon_api_config()

        self.headers = {
            "Content-Type": "application/json",
        }
        self.AuthToken = "default-token-used-in-server-side"
        self.ApiToken = j.dumps({"name": "monitor", "sig": "default-token-used-in-server-side"})

        self.base_url = self._get_base_url()

    def _get_base_url(self):
        return self.falcon_api_config.get("plus_api", "")

    @staticmethod
    def _get_falcon_api_config():
        return config.CONF.to_dict().get("falcon_api") or {}

    def get_falcon_api_common(self, url, params=None, token_key="", token="", timeout = 5):
        headers = copy.deepcopy(self.headers)
        if token_key:
            headers[token_key] = token
        else:
            headers["X-Auth-Token"] = self.AuthToken
        url = self.base_url + url
        ret = HttpHelper(url, timeout=timeout, header=headers).http_get(params2=params)
        return ret.json()

    def post_falcon_api_common(self, url, params=None, decode_json=None, json_data=None, token_key="", token=""):
        headers = copy.deepcopy(self.headers)
        if token_key:
            headers[token_key] = token
        else:
            headers["X-Auth-Token"] = self.AuthToken
        url = self.base_url + url
        ret = HttpHelper(url, timeout=5, header=headers).http_post(params=params,decode_json=decode_json,json_data=json_data)
        return ret.json()

    def get_project_id_by_node_ids(self, node_ids, is_all):
        """
        根据node_ids获取project
        :param node_ids: 行政组织id list
        :param is_all: 全选标准层级
        :return: list
        """
        if is_all:
            url = "/cloud/v1/auth/projects?organization_id__notnull=true"
        elif node_ids:
            params = ",".join(node_ids) if isinstance(node_ids, list) else node_ids
            url = "/cloud/v1/auth/projects?organization_id=%s" % params
        else:
            return []
        res = self.get_falcon_api_common(url,timeout= 15)
        data = res.get("data")
        if not data:
            return []
        return [str(item.get("id")) for item in data if item.get("id")]

    def get_tenant_id_by_node_ids(self, node_ids):
        """
        根据node_ids自定义层级获取tenant_id
        :param node_ids: 行政组织id list
        :return: list
        """
        params = ",".join(node_ids) if isinstance(node_ids, list) else node_ids
        url = "/cloud/v1/tenant_tree/classify_filter?node_ids=%s" % params
        res = self.get_falcon_api_common(url)
        data = res.get("tenant_id")
        if not data:
            return []
        return [str(i) for i in data]

    def get_tenant_info(self, tenant_id):
        """
        根据tenant_id获取租户信息
        :param tenant_id:
        :return: dict
        """
        url = "/cloud/v1/auth/tenants?id=%s" % tenant_id
        res = self.get_falcon_api_common(url)
        data = res.get("data")
        if not data:
            return {}
        return data[0]

    def get_project_info(self, project_id):
        """
        根据project_id获取租户信息
        :param project_id:
        :return: dict
        """
        url = "/cloud/v1/auth/projects?id=%s" % project_id
        res = self.get_falcon_api_common(url)
        data = res.get("data")
        if not data:
            return {}
        return data[0]

    def get_last_point_by_graph(self, params):
        """
               根据endpoint和counter查询,返回最新的graph记录
               :param params:[{
                   "endpoint": endpoint,
                   "counter": counter
               },{}]
               :return:
        """
        url = "/api/v1/graph/lastpoint"
        res = self.post_falcon_api_common(url, json_data=params, token_key="Apitoken", token=self.ApiToken)
        return res

    def get_counter(self, endpoint, metric):
        """
               根据endpoint和metric查询 counter
        """
        if isinstance(endpoint, list):
            endpoint = ",".join(endpoint)

        url = "/api/v1/index/counters?" + "e=" + endpoint + "&m=" + metric
        res = self.get_falcon_api_common(url, token_key="Apitoken", token=self.ApiToken)
        return res
