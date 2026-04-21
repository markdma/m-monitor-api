# coding: utf-8
import copy

import falcon

from monitor.apps.collect_cfg.api import collect_cfg_api

from monitor.common.controller import CollectionController, ItemController
from monitor.common import time_util, const_define
from monitor.core.exceptions import ValidationError, NotFoundError, ForbiddenError
from monitor.lib.validation import check_params_with_model
from monitor.apps.auth.api import user_api

import logging


class CollectCfgManageBase(object):

    @staticmethod
    def _arg_model_update_data():
        base_define = {
            "tags": {"type": basestring, "notnull": True, "required": False, "format": {">=": 0, "<": 256}},
            "nid": {"type": int, "notnull": True, "required": False, "format": {">": 0}},
            "file_path": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}},
            "time_format": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 128}},
            "pattern": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 1024}},
            "func": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 65}},
            "timeout": {"type": int, "notnull": True, "required": False, "format": {">": 0, "<": 65536}},
            "comment": {"type": basestring, "notnull": True, "required": False, "format": {">=": 0, "<": 512}},
            "collect_method": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 65}},
            "last_updator": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "step": {"type": int, "notnull": True, "required": False, "format": {">": 9, "<": 65536}},
            "collect_name": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 256}}
        }
        return base_define

    @staticmethod
    def _arg_model_create_log_data():
        base_define = {
            "nid": {"type": int, "notnull": True, "required": True, "format": {">": 0}},
            "name": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "collect_name": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "tags": {"type": basestring, "notnull": True, "required": False, "format": {">=": 0, "<": 256}},
            "collect_type": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 65}},
            "step": {"type": int, "notnull": True, "required": True, "format": {">": 9, "<": 65536}},
            "file_path": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "time_format": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 128}},
            "pattern": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 1024}},
            "func": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 65}},
            "degree": {"type": int, "notnull": True, "required": False, "format": {">": 0}},
            "comment": {"type": basestring, "notnull": True, "required": False, "format": {">=": 0, "<": 512}},
            "creator": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}}
        }
        return base_define

    @staticmethod
    def _arg_model_create_port_data():
        base_define = {
            "nid": {"type": int, "notnull": True, "required": True, "format": {">": 0}},
            "name": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "collect_name": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "tags": {"type": basestring, "notnull": True, "required": False, "format": {">=": 0, "<": 256}},
            "collect_type": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 65}},
            "step": {"type": int, "notnull": True, "required": True, "format": {">": 9, "<": 65536}},
            "port": {"type": int, "notnull": True, "required": True, "format": {">": 0, "<": 65536}},
            "timeout": {"type": int, "notnull": True, "required": False, "format": {">": 0, "<": 65536}},
            "comment": {"type": basestring, "notnull": True, "required": False, "format": {">=": 0, "<": 512}},
            "creator": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}}
        }
        return base_define

    @staticmethod
    def _arg_model_create_porc_data():
        base_define = {
            "nid": {"type": int, "notnull": True, "required": True, "format": {">": 0}},
            "name": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "collect_name": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "tags": {"type": basestring, "notnull": True, "required": False, "format": {">=": 0, "<": 256}},
            "collect_type": {"type": basestring, "notnull": True, "required": False, "format": {">": 0, "<": 65}},
            "collect_method": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 65}},
            "target": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}},
            "step": {"type": int, "notnull": True, "required": True, "format": {">": 9, "<": 65536}},
            "comment": {"type": basestring, "notnull": True, "required": False, "format": {">=": 0, "<": 512}},
            "creator": {"type": basestring, "notnull": True, "required": True, "format": {">": 0, "<": 256}}
        }
        return base_define



class CollectCfgManageController(CollectionController, CollectCfgManageBase):
    name = 'monitor.collect_cfg'
    allow_methods = ('GET', 'POST')
    resource = collect_cfg_api.CollectLogCfgManageApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        filters = criteria["filters"]

        #logging.info(criteria)
        if "collect_type" in filters.keys():
            collect_type = filters.pop("collect_type", None)
            if collect_type == const_define.CollectType.Log:
                collect_type_api = collect_cfg_api.CollectLogCfgManageApi()
            elif collect_type == const_define.CollectType.Port:
                collect_type_api = collect_cfg_api.CollectPortCfgManageApi()
            elif collect_type == const_define.CollectType.Proc:
                collect_type_api = collect_cfg_api.CollectProcCfgManageApi()
            else:
                raise ValidationError("params参数 collect_type: %s, 必须在%s 中" % (collect_type, const_define.CollectType.ALL_TYPE))
        else:
            raise ValidationError("params参数 stat_type: 不能为空")

        fields = criteria.pop('fields', None)
        limit = filters.pop("size", None)
        offset = filters.pop("page", None)
        criteria["limit"] = int(limit) if limit else limit
        criteria["offset"] = (int(offset) - 1) * 10 if offset else offset
        refs = collect_type_api.list(**criteria)
        get_user_api = user_api.UserManageApi()
        for ref in refs:
            creator_id = ref["creator"]
            if creator_id:
                creator = get_user_api.list(filters={"uid": creator_id})
                if creator:
                    creator = creator[0].get("name")
                ref["creator"] = creator if creator else creator_id
            updator_id = ref["last_updator"]
            if updator_id:
                last_updator = get_user_api.list(filters={"uid": updator_id})
                if last_updator:
                    last_updator = last_updator[0].get("name")
                ref["last_updator"] = last_updator if last_updator else updator_id

        if fields is not None:
            refs = [self._simplify_info(ref, fields) for ref in refs]
        count = collect_type_api.count(filters)
        resp.json = {'count': count, 'data': refs}

    def on_post(self, req, resp, **kwargs):
        self._validate_method(req)
        req_json_data = req.json
        if "collect_type" not in req_json_data.keys():
            raise ValidationError("params参数 collect_type: 不能为空")

        collect_type = req_json_data.get("collect_type")
        #logging.info(req.json)
        if collect_type == const_define.CollectType.Log:
            #logging.info("log")
            collect_type_api = collect_cfg_api.CollectLogCfgManageApi()
            if not req.json.get("degree"):
                req.json["degree"] = 6
            checked_data = check_params_with_model(req.json, self._arg_model_create_log_data(), keep_extra_key=False)
        elif collect_type == const_define.CollectType.Port:
            collect_type_api = collect_cfg_api.CollectPortCfgManageApi()
            checked_data = check_params_with_model(req.json, self._arg_model_create_port_data(), keep_extra_key=False)
        elif collect_type == const_define.CollectType.Proc:
            collect_type_api = collect_cfg_api.CollectProcCfgManageApi()
            checked_data = check_params_with_model(req.json, self._arg_model_create_porc_data(), keep_extra_key=False)
        else:
            raise ValidationError(
                "params参数 collect_type: %s, 必须在%s 中" % (collect_type, const_define.CollectType.ALL_TYPE))

        #logging.info(checked_data)
        resp.json = collect_type_api.create(checked_data)
        resp.status = falcon.HTTP_201


class CollectCfgItemManageController(ItemController, CollectCfgManageBase):
    name = 'monitor.collect_cfg.item'
    allow_methods = ('PATCH', 'GET', 'DELETE')
    resource = collect_cfg_api.CollectLogCfgManageApi


    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        cfg_id = kwargs.pop('rid')

        criteria = self._build_criteria(req)
        filters = criteria["filters"]
        #logging.info(criteria)
        if "collect_type" in filters.keys():
            collect_type = filters.pop("collect_type", None)
            if collect_type == const_define.CollectType.Log:
                collect_type_api = collect_cfg_api.CollectLogCfgManageApi()
            elif collect_type == const_define.CollectType.Port:
                collect_type_api = collect_cfg_api.CollectPortCfgManageApi()
            elif collect_type == const_define.CollectType.Proc:
                collect_type_api = collect_cfg_api.CollectProcCfgManageApi()
            else:
                raise ValidationError("params参数 collect_type: %s, 必须在%s 中" % (collect_type, const_define.CollectType.ALL_TYPE))
        else:
            raise ValidationError("params参数 collect_type: 不能为空")

        cfg_info = collect_type_api.get(cfg_id)
        if not cfg_info:
            raise NotFoundError("cfg_id:%s不存在" % cfg_id)
        get_user_api = user_api.UserManageApi()
        creator_id = cfg_info["creator"]
        if creator_id:
            creator = get_user_api.list(filters={"uid": creator_id})
            if creator:
                creator = creator[0].get("name")
            cfg_info["creator"] = creator if creator else creator_id
        updator_id = cfg_info["last_updator"]
        if updator_id:
            last_updator = get_user_api.list(filters={"uid": updator_id})
            if last_updator:
                last_updator = last_updator[0].get("name")
            cfg_info["last_updator"] = last_updator if last_updator else updator_id
        resp.json = cfg_info


    def on_patch(self, req, resp, **kwargs):
        self._validate_method(req)
        cfg_id = kwargs.pop('rid')

        req_json_data = req.json
        if "collect_type" not in req_json_data.keys():
            raise ValidationError("params参数 collect_type: 不能为空")

        collect_type = req_json_data.get("collect_type")
        if collect_type == const_define.CollectType.Log:
            collect_type_api = collect_cfg_api.CollectLogCfgManageApi()
        elif collect_type == const_define.CollectType.Port:
            collect_type_api = collect_cfg_api.CollectPortCfgManageApi()
        elif collect_type == const_define.CollectType.Proc:
            collect_type_api = collect_cfg_api.CollectProcCfgManageApi()
        else:
            raise ValidationError(
                "params参数 collect_type: %s, 必须在%s 中" % (collect_type, const_define.CollectType.ALL_TYPE))

        cfg_info = collect_type_api.get(cfg_id)
        if not cfg_info:
            raise NotFoundError("cfg_id: %s, 不存在" % cfg_id)
        checked_data = check_params_with_model(req_json_data, self._arg_model_update_data(), keep_extra_key=False)
        if not checked_data:
            resp.json = cfg_info
        else:
            before, after = collect_type_api.update(cfg_id, checked_data)
            resp.json = after

    def on_delete(self, req, resp, **kwargs):
        self._validate_method(req)
        try:
            cfg_id = kwargs.pop('rid')
        except KeyError as e:
            raise NotFoundError("rid:%s不存在参数中" % kwargs)
        req_json_data = req.params

        if "collect_type" not in req_json_data.keys():
            raise ValidationError("params参数 collect_type: 不能为空")

        collect_type = req_json_data.get("collect_type")
        if collect_type == const_define.CollectType.Log:
            collect_type_api = collect_cfg_api.CollectLogCfgManageApi()
        elif collect_type == const_define.CollectType.Port:
            collect_type_api = collect_cfg_api.CollectPortCfgManageApi()
        elif collect_type == const_define.CollectType.Proc:
            collect_type_api = collect_cfg_api.CollectProcCfgManageApi()
        else:
            raise ValidationError(
                "params参数 collect_type: %s, 必须在%s 中" % (collect_type, const_define.CollectType.ALL_TYPE))

        cfg_info = collect_type_api.get(cfg_id)
        if not cfg_info:
            raise NotFoundError("cfg_id:%s不存在" % cfg_id)

        count, data = collect_type_api.delete(cfg_id)
        resp.json = {'count': count, 'data': data}







