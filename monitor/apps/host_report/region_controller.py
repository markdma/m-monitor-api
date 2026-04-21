# coding: utf-8
import copy

from monitor.apps.host_report.api import region_api, az_api
from monitor.common.controller import CollectionController, ItemController
from monitor.core.exceptions import NotFoundError
from monitor.lib.validation import check_params_with_model


class RegionBase(object):

    @staticmethod
    def _arg_model_update_data():
        base_define = {
            "is_using": {"type": int, "notnull": False, "required": False, "format": {"in": [0, 1]}}
        }
        return base_define


class RegionController(CollectionController):
    name = 'monitor.if_region'
    allow_methods = ('GET',)
    resource = region_api.RegionApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        criteria = self._build_criteria(req)
        refs = self.list(req, copy.deepcopy(criteria), **kwargs)
        count = self.count(req, criteria, results=refs, **kwargs)
        resp.json = {'count': count, 'data': refs}


class RegionItemController(ItemController, RegionBase):
    name = 'monitor.if_region'
    allow_methods = ('GET', 'PATCH',)
    resource = region_api.RegionApi

    def on_get(self, req, resp, **kwargs):
        region_id = kwargs.pop('rid')
        api = self.make_resource(req)
        region_info = api.get(region_id)
        if not region_info:
            raise NotFoundError("region id:%s不存在" % region_id)
        resp.json = region_info

    def on_patch(self, req, resp, **kwargs):
        region_id = kwargs.pop('rid')
        api = self.make_resource(req)
        region_info = api.get(region_id)
        if not region_info:
            raise NotFoundError("region id:%s不存在" % region_id)

        checked_data = check_params_with_model(req.json, self._arg_model_update_data(), keep_extra_key=False)
        if not checked_data:
            resp.json = region_info
        else:
            before, after = api.update(region_id, checked_data)
            resp.json = after


class RegionAZController(CollectionController):
    name = 'monitor.if_region_azs'
    allow_methods = ('GET',)
    resource = region_api.RegionApi

    def on_get(self, req, resp, **kwargs):
        self._validate_method(req)
        api_region = region_api.RegionApi()
        api_az = az_api.AvailableZoneApi()
        region_list = api_region.list(filters={"is_using": 1})
        region_dict = {info["id"]: info for info in region_list}
        az_list = api_az.list(filters={"region_id": region_dict.keys()})
        for az_info in az_list:
            if az_info and isinstance(az_info, dict):
                az_info.pop("region", None)
            region_id = az_info["region_id"]
            if region_id and region_id in region_dict and isinstance(region_dict[region_id], dict):
                if region_dict[region_id].has_key("azs") and isinstance(region_dict[region_id]["azs"], list):
                    region_dict[region_id]["azs"].append(az_info)
                else:
                    region_dict[region_id]["azs"] = [az_info]
        resp.json = {'count': len(region_dict), 'data': region_dict.values()}
