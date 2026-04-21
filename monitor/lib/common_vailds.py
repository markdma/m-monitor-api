# coding: utf-8
import re

from monitor.core import exceptions


def validate_mobile_format(mobile, area_code=None):
    """
    校验手机号码的工具方法，暂时涉及大陆，香港
    如果不传area_code, 默认大陆
    :param mobile:
    :param area_code:
    :return:
    """
    mapping_dict = {
        "china": r"^1[356789]\d{9}$",
        "hongkong": r"^(5|6|8|9)\d{7}$"
    }
    if area_code is None:
        if not re.match(mapping_dict.get('china'), mobile):
            raise exceptions.ValidationError("手机号码格式不正确")
        return mobile
    if area_code not in mapping_dict:
        raise exceptions.ValidationError("手机地区码不存在")
    if not re.match(mapping_dict.get(area_code), mobile):
        raise exceptions.ValidationError("手机号码格式不正确")
    return mobile