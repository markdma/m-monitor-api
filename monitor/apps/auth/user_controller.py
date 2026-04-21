# coding: utf-8
import copy

import falcon

from monitor.apps.auth.api import user_api
from monitor.apps.auth.dbresources.resource import UserManageResource, UserPolicyManageResource
from monitor.common.common_check import UserCheck
from monitor.common.controller import ItemController, CollectionController
from monitor.lib.validation import check_params_with_model
from monitor.core.exceptions import NotFoundError, ValidationError


class UserBase(object):

    def _arg_model_update_data(self):
        define = {
            "phone": {"type": basestring, "notnull": False, "required": False, "format": {">": 0, "<": 16}}
        }
        return define

    def get_user_info(self, user_id):
        user_info = UserManageResource().get(user_id)
        if not user_info:
            raise NotFoundError("user id :%s,不存在")
        return user_info

    def check_phone(self, phone):
        result, new_phone, country_code = UserCheck().validate_phone(phone)
        if not result:
            raise ValidationError("phone:%s,非法的手机号码" % phone)
        return new_phone


class UserItemController(ItemController, UserBase):
    name = 'auth.user.item'
    allow_methods = ('PATCH', 'GET')
    resource = user_api.UserManageApi

    def on_patch(self, req, resp, **kwargs):
        self._validate_method(req)
        user_id = kwargs.get("rid")
        user_info = self.get_user_info(user_id)
        check_data = check_params_with_model(req.json, self._arg_model_update_data(), keep_extra_key=False)
        if not check_data:
            resp.json = user_info
        else:
            if check_data.get('phone', None):
                check_data['phone'] = self.check_phone(check_data['phone'])
            user_api_handler = self.make_resource(req)
            before, after = user_api_handler.update(user_id, check_data)
            resp.json = after

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        user_id = kwargs.pop('rid')
        user_info = self.get_user_info(user_id)
        resp.json = user_info


class UserController(CollectionController, UserBase):
    name = 'auth.user'
    allow_methods = ('GET',)
    resource = user_api.UserManageApi


class UserPolicyBase(object):

    @staticmethod
    def _arg_model_create_data():
        base_define = {
            "url": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 101}},
            "method": {"type": basestring, "notnull": True, "required": True,
                       "format": {"in": ["GET", "POST", "DELETE", "PATCH", "PUT"]}},
            "name": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 65}},
            "is_default": {"type": int, "notnull": False, "required": False, "format": {"in": [0, 1]}}
        }
        return base_define

    @staticmethod
    def _arg_model_update_data():
        base_define = {
            "url": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 101}},
            "method": {"type": basestring, "notnull": True, "required": False,
                       "format": {"in": ["GET", "POST", "DELETE", "PATCH", "PUT"]}},
            "name": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 65}},
            "is_default": {"type": int, "notnull": True, "required": False, "format": {"in": [0, 1]}}
        }
        return base_define

    @staticmethod
    def check_url_method(url, method, expire_self_flag=False, policy_id=None):
        """对url与请求方式做唯一性校验"""
        if url and method:
            if expire_self_flag and policy_id:
                result = UserPolicyManageResource().list(filters={"url": url, "method": method, "is_deleted": 0,
                                                                  "id": {"ne": policy_id}})
            else:
                result = UserPolicyManageResource().list(filters={"url": url, "method": method, "is_deleted": 0})
            if result and len(result) >= 1:
                raise ValidationError("url与method组合已存在")

    @staticmethod
    def check_name(name, expire_self_flag=False, policy_id=None):
        """对name做唯一性校验"""
        if name:
            if expire_self_flag and policy_id:
                result = UserPolicyManageResource().list(filters={"name": name, "is_deleted": 0, "id": {"ne": policy_id}})
            else:
                result = UserPolicyManageResource().list(filters={"name": name, "is_deleted": 0})
            if result and len(result) >= 1:
                raise ValidationError("name已存在")

    @staticmethod
    def _arg_model_mapping():
        """替换请求params中的敏感词"""
        base_define = {
            "ON_GET": "GET",
            "ON_POST": "POST",
            "ON_PUT": "PUT",
            "ON_DELETE": "DELETE",
            "DEL": "DELETE",
            "ON_PATCH": "PATCH"
        }
        return base_define

    @staticmethod
    def replace_args_name(mapping_value, replace_dict):
        if isinstance(mapping_value, dict) and isinstance(replace_dict, dict):
            for k, v in replace_dict.items():
                if v and str(v) in mapping_value:
                    replace_dict[k] = mapping_value[str(v)]
        return replace_dict


class UserPolicyController(CollectionController, UserPolicyBase):
    name = 'auth.user_policies'
    allow_methods = ('GET', 'POST')
    resource = user_api.UserPolicyManageApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        filters_new = self.replace_args_name(self._arg_model_mapping(), filters)
        criteria["filters"] = filters_new
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}

    def on_post(self, req, resp, **kwargs):
        self._validate_method(req)
        checked_data = check_params_with_model(req.json, self._arg_model_create_data(), keep_extra_key=False)
        self.check_url_method(checked_data.get("url"), checked_data.get("method"))
        self.check_name(checked_data.get("name"))
        user_policy_api = self.make_resource(req)
        resp.json = user_policy_api.create(checked_data)
        resp.status = falcon.HTTP_201


class UserPolicyItemController(ItemController, UserPolicyBase):
    name = 'auth.user_policies.item'
    allow_methods = ('GET', 'PATCH', 'DELETE')
    resource = user_api.UserPolicyManageApi

    def on_get(self, req, resp, **kwargs):
        user_policy_id = kwargs.pop('rid')
        api = self.make_resource(req)
        user_policy_info = api.get(user_policy_id)
        if not user_policy_info:
            raise NotFoundError("user policy id:%s不存在" % user_policy_id)
        resp.json = user_policy_info

    def on_patch(self, req, resp, **kwargs):
        user_policy_id = kwargs.pop('rid')
        api = self.make_resource(req)
        user_policy_info = api.get(user_policy_id)
        if not user_policy_info:
            raise NotFoundError("user policy id:%s不存在" % user_policy_id)

        checked_data = check_params_with_model(req.json, self._arg_model_update_data(), keep_extra_key=False)
        if not checked_data:
            resp.json = user_policy_info
        else:
            if checked_data.get("url") or checked_data.get("method"):
                url = checked_data.get("url") or user_policy_info["url"]
                method = checked_data.get("method") or user_policy_info["method"]
                self.check_url_method(url, method, expire_self_flag=True, policy_id=user_policy_id)
            if checked_data.get("name"):
                self.check_name(checked_data.get("name"), expire_self_flag=True, policy_id=user_policy_id)
            before, after = api.update(user_policy_id, checked_data)
            resp.json = after

    def on_delete(self, req, resp, **kwargs):
        user_policy_id = kwargs.pop('rid')
        api = self.make_resource(req)
        user_policy_info = api.get(user_policy_id)
        if not user_policy_info:
            raise NotFoundError("user policy id:%s不存在" % user_policy_id)
        count, data = api.delete(user_policy_id)
        resp.json = {'count': count, 'data': data}
