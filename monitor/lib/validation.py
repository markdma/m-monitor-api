# _ coding:utf-8 _*_
# author = "rd"

"""
本模块，提供参数校验，检查不符合条件请求参数
格式如下：
adb = {
    "id": {"type": int, "notnull": False, "format": {">": 0, "<": 255, "in": [1, 2, 3, 4]}},
    "name": {"type": basestring, "notnull": False, "format": {">": 2, "<": 255, "re.match":"[a-z]"}},
    "desc": {"type": datetime.datetime},
    "status": {"type": bool},
    "ss": {"type": list, "notnull": True, "format": {"size":{">": 2, "<": 255}, "lenth":{">": 2, "<": 255},"in":[], "re.match":"[a-z]"}},
    "ggg": {"type": dict},
    "cv": {"type": "ip"},
    "xcss": {"type": "email"},
    "confs": {"type": list, "notnull": True, "format": {"lenth":{">": 2, "<": 255},
                                                        "recursive_model":{"name": {"type": basestring,"format": {">": 2, "<": 255}}}
                                                        },
    detail: {"type": dict, "format": {"lenth":{">": 2, "<": 255},
                                    "recursive_model":{"age": {"type": int,"format": {">": 2, "<": 255}}}
                                    }
}
type字段为必须定义
format 定义简单的数值大小及字段长度的检查，in表示只允许固定的一些值，为列表类型
notnull 代表是否不为null， True表示不为None

新增：可校验列表嵌套的字典与value为字典的数据，需要在对应的format里面添加一个recursive_model，model的各个键为嵌套字典的需要校验的键

注：数据库自增型字段不要定义，或自动生成的字段不要定义

:return 处理后的字段，如有不符合条件的字段，则会抛出ValidationError异常
"""

import re
import datetime
from monitor.lib.ip_address import check_ip
from monitor.core.exceptions import ValidationError
from monitor.core.i18n import _

args_type = {
    "int": "整数",
    "float": "浮点数",
    "list": "列表",
    "dict": "json类型",
    "basestring": "字符串类型",
    "str": "字符串类型",
    "unicode": "字符串类型",
    "bool": "布尔值",
    "datetime.datetime": "时间类型",
    "long": "长整型"
}


def _type_to_utf8(type):
    for ixe in args_type.keys():
        if type == eval(ixe):
            return args_type.get(ixe)


def str_to_time(date_str):
    if ":" in date_str:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')


def check_email_address(email_address):
    if not isinstance(email_address, basestring):
        raise ValidationError("email类型错误，必须为字符串类型")
    if re.match(r'^[\.a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email_address):
        return True
    else:
        return False


def v_va(key, value, model, allow_bool_null=False):
    if key not in model.keys():
        # 允许传多参数
        model.pop(key,None)
        return
        # raise ValidationError("非法的参数: %s" % key)

    format_type = model.get(key).get("type")
    if value is None:
        if allow_bool_null is False and format_type == bool:
            raise ValidationError("bool 值不允许为空 ")
        if model.get(key).get("notnull"):
            raise ValidationError("%s 不允许为空" % key)
        else:
            return value
    if format_type == datetime.datetime:
        if isinstance(value, basestring):
            if "/" in value:
                value = value.replace("/", "-")
            value = str_to_time(value)

    if format_type == int:
        if value is None:
            return value
        else:
            try:
                value = int(value)
            except:
                raise ValidationError("%s 不是整数" % (key))

    if format_type == "ip":
        res, msg = check_ip(value)
        if res:
            return value
        else:
            raise ValidationError("%s 不是合法IP地址" % (key))

    if format_type == "email":
        res = check_email_address(value)
        if res:
            return value
        else:
            raise ValidationError("%s 不是合法的email地址" % (value))

    if isinstance(value, format_type):
        format_data = model.get(key).get("format", {})
        if format_data:
            if format_type == int:
                if format_data.get(">") is not None:
                    if not value > format_data.get(">"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须大于 %s" % (key, value, format_data.get(">")))
                if "<" in format_data:
                    if not value < format_data.get("<"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须小于 %s" % (key, value, format_data.get("<")))
                if ">=" in format_data:
                    if not value >= format_data.get(">="):
                        raise ValidationError("%s 非法值: %s，参数值必须大于等于%s" % (key, value, format_data.get(">=")))
                if "<=" in format_data:
                    if not value <= format_data.get("<="):
                        raise ValidationError("%s 非法值: %s，参数值必须小于等于%s" % (key, value, format_data.get("<=")))
                if "in" in format_data:
                    if value not in format_data.get("in"):
                        raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))
            if format_type == basestring:
                if format_data.get(">") is not None:
                    if not len(value) > format_data.get(">"):
                        raise ValidationError("%s 非法值： %s, 参数长度必须大于 %s" % (
                            key, len(value), format_data.get(">")))
                if "<" in format_data:
                    if not len(value) < format_data.get("<"):
                        raise ValidationError("%s 非法值： %s, 参数长度必须小于 %s" % (
                            key, len(value), format_data.get("<")))
                if format_data.get(">=") is not None:
                    if not len(value) >= format_data.get(">="):
                        raise ValidationError("%s 非法值： %s, 参数长度必须大于等于 %s" % (
                            key, len(value), format_data.get(">=")))
                if format_data.get("<=") is not None:
                    if not len(value) <= format_data.get("<="):
                        raise ValidationError("%s 非法值： %s, 参数长度必须小于等于 %s" % (
                            key, len(value), format_data.get("<=")))
                if format_data.get("==") is not None:
                    if not len(value) == format_data.get("=="):
                        raise ValidationError("%s 非法值： %s, 参数长度必须等于 %s" % (
                            key, len(value), format_data.get("==")))
                if "in" in format_data:
                    if value not in format_data.get("in"):
                        raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))

                if "re.match" in format_data:
                    if not re.match(r'%s' % format_data.get("re.match"), value):
                        raise ValidationError("%s 非法值： %s, 不符合规则" % (key, value))

            if format_type == list:
                if "size" in format_data:
                    size_data = format_data.get("size")
                    if size_data.get(">") is not None:
                        le_value = size_data.get(">")
                        for t_value in value:
                            if isinstance(t_value, int):
                                if not t_value > le_value:
                                    raise ValidationError("%s 非法值： %s, 参数值必须大于 %s" % (
                                        key, t_value, le_value))
                            if isinstance(t_value, basestring):
                                if not len(t_value) > le_value:
                                    raise ValidationError("%s 非法值： %s, 参数长度必须大于 %s" % (
                                        key, len(t_value), le_value))
                    if "<" in size_data:
                        le_value = size_data.get("<")
                        for t_value in value:
                            if isinstance(t_value, int):
                                if not t_value < le_value:
                                    raise ValidationError("%s 非法值： %s, 参数值必须小于 %s" % (
                                        key, t_value, le_value))
                            if isinstance(t_value, basestring):
                                if not len(t_value) < le_value:
                                    raise ValidationError("%s 非法值： %s, 参数长度必须小于 %s" % (
                                        key, len(t_value), le_value))
                if "lenth" in format_data:
                    lenth_data = format_data.get("lenth")
                    len_list = len(value)
                    if lenth_data.get(">") is not None:
                        if not len_list > lenth_data.get(">"):
                            raise ValidationError("%s 非法长度：%s 列表长度必须大于 %s" % (
                                key, len_list, lenth_data.get(">")))
                    if "<" in lenth_data:
                        if not len_list < lenth_data.get("<"):
                            raise ValidationError("%s 非法长度：%s 列表长度必须小于 %s" % (
                                key, len_list, lenth_data.get("<")))

                if "in" in format_data:
                    le_value = format_data.get("in")
                    for t_value in value:
                        if t_value not in le_value:
                            raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))

                if "re.match" in format_data:
                    rematch = format_data.get("re.match")
                    for t_value in value:
                        if not re.match(r'%s' % rematch, t_value):
                            raise ValidationError("%s 非法值： %s, 不符合规则" % (key, value))

        return value
    else:
        raise ValidationError("非法类型参数， 参数 %s 传入类型为 %s, 合法类型必须为： %s"
            % (key, _type_to_utf8(type(value)), _type_to_utf8(format_type)))


def model_via_check(dictstr, model, necessary=True, keep_extra_key=True, allow_bool_null=False):
    if not isinstance(dictstr, dict):
        raise ValidationError("data不为json类型")
    if not isinstance(model, dict):
        raise ValidationError("model不为字典类型")
    if len(dictstr) == 0:
        return dictstr

    if not model:
        return dictstr

    if necessary:
        for ixc in model.keys():
            if model.get(ixc).get("notnull"):
                if ixc not in dictstr.keys():
                    raise ValidationError("缺少必填参数: %s" % ixc)
                else:
                    if dictstr.get(ixc) is None:
                        raise ValidationError("参数: %s 不允许为空" % ixc)

    _dict = {}
    for key in dictstr.keys():
        v = v_va(key, dictstr.get(key), model, allow_bool_null)
        if v is None and keep_extra_key is False:
            continue
        _dict[key] = v

    return _dict


def check_params_with_model(dictstr, model, keep_extra_key=False, necessary=True, strip_null_str=False, **kwargs):
    """
    注：参数中的两个字段required， notnull。
    如果有required， 并且值为True, 则是必传参数
    如果有notnull， 并且值为True，则传入的参数不能为空
    :param dictstr:需要校验的参数（dict）
    :param model:校验模型
    :param necessary:是否必要，如果为否，则不校验参数的必要性
    :param strip_null_str:移除字符串首尾的空字符串
    :return:
    """
    if not isinstance(dictstr, dict):
        raise ValidationError("data不为json类型")
    if not isinstance(model, dict):
        raise ValidationError("model不为字典类型")
    if not dictstr or not model:
        return dictstr

    if necessary:
        for ixc in model.keys():
            if model.get(ixc).get("required"):
                if ixc not in dictstr.keys():
                    raise ValidationError("%s缺少必填参数: %s" % (kwargs.get("parent_key", ''), ixc))

    for ixc in model.keys():
        if model.get(ixc).get("notnull"):
            # 如果这个字段传入，但是值为None，则抛出异常，如果不传，则不处理
            if ixc in dictstr.keys():
                if dictstr.get(ixc) is None:
                    raise ValidationError("参数不能为空: %s" % ixc)

    _dict = {}
    for key in dictstr.keys():
        v = v_vv(key, dictstr.get(key), model, keep_extra_key=keep_extra_key, necessary=necessary, strip_null_str=strip_null_str)
        if v == "not__exist__in__model":
            if keep_extra_key is False:
                pass
            else:
                _dict[key] = dictstr.get(key)
            continue
        _dict[key] = v
    return _dict


def v_vv(key, value, model, keep_extra_key=False, necessary=True, strip_null_str=False):
    if key not in model.keys():
        # 允许传多参数
        model.pop(key, None)
        # 这里返回一个标记，用于说明当前的参数不在model中
        return "not__exist__in__model"

    format_type = model.get(key).get("type")
    if format_type == datetime.datetime:
        if isinstance(value, basestring):
            if "/" in value:
                value = value.replace("/", "-")
            value = str_to_time(value)
    elif format_type == "datetime":
        if isinstance(value, basestring):
            if "/" in value:
                value = value.replace("/", "-")
            try:
                value = str_to_time(value)
                return value
            except:
                raise ValidationError("%s 时间格式不正确" % (key))

    if format_type == int:
        if value is None:
            return value
        else:
            if not isinstance(value, int):
                raise ValidationError("%s 不是整数" % (key))

    if format_type == float:
        if value is None:
            return value
        else:
            if isinstance(value, int):
                # 如果是浮点数类型，如果value是整数，value转化为浮点数
                value = float(value)
            elif isinstance(value, float):
                pass
            else:
                raise ValidationError("%s 不是浮点数" % (key))

    if format_type == basestring:
        if value is None:
            return value
        else:
            if not isinstance(value, basestring):
                raise ValidationError("%s 不是字符串类型" % (key))
            if strip_null_str is True:
                value = value.strip()

    if format_type == dict:
        if value is None:
            return value
        else:
            if not isinstance(value, dict):
                raise ValidationError("%s 不是字典类型" % (key))

    if format_type == list:
        if value is None:
            return value
        else:
            if not isinstance(value, list):
                raise ValidationError("%s 不是列表类型" % (key))

    if format_type == "ip":
        res, msg = check_ip(value)
        if res:
            return value
        else:
            raise ValidationError("%s 不是合法IP地址" % (key))

    if format_type == "email":
        res = check_email_address(value)
        if res:
            return value
        else:
            raise ValidationError("%s 不是合法的email地址" % (value))

    if isinstance(value, format_type):
        format_data = model.get(key).get("format", {})
        if format_data:
            if format_type == int:
                if format_data.get(">") is not None:
                    if not value > format_data.get(">"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须大于 %s" % (key, value, format_data.get(">")))
                if "<" in format_data:
                    if not value < format_data.get("<"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须小于 %s" % (key, value, format_data.get("<")))
                if ">=" in format_data:
                    if not value >= format_data.get(">="):
                        raise ValidationError("%s 非法值: %s，参数值必须大于等于%s" % (key, value, format_data.get(">=")))
                if "<=" in format_data:
                    if not value <= format_data.get("<="):
                        raise ValidationError("%s 非法值: %s，参数值必须小于等于%s" % (key, value, format_data.get("<=")))
                if "in" in format_data:
                    if value not in format_data.get("in"):
                        raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))
            if format_type == float:
                if format_data.get(">") is not None:
                    if not value > format_data.get(">"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须大于 %s" % (key, value, format_data.get(">")))
                if "<" in format_data:
                    if not value < format_data.get("<"):
                        raise ValidationError(
                            "%s 非法值： %s, 参数值必须小于 %s" % (key, value, format_data.get("<")))
                if ">=" in format_data:
                    if not value >= format_data.get(">="):
                        raise ValidationError("%s 非法值: %s，参数值必须大于等于%s" % (key, value, format_data.get(">=")))
                if "<=" in format_data:
                    if not value <= format_data.get("<="):
                        raise ValidationError("%s 非法值: %s，参数值必须小于等于%s" % (key, value, format_data.get("<=")))
                if "in" in format_data:
                    if value not in format_data.get("in"):
                        raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))
            if format_type == basestring:
                if format_data.get(">") is not None:
                    if not len(value) > format_data.get(">"):
                        raise ValidationError("%s 非法值： %s, 参数长度必须大于 %s" % (
                            key, len(value), format_data.get(">")))
                if "<" in format_data:
                    if not len(value) < format_data.get("<"):
                        raise ValidationError("%s 非法值： %s, 参数长度必须小于 %s" % (
                            key, len(value), format_data.get("<")))
                if format_data.get(">=") is not None:
                    if not len(value) >= format_data.get(">="):
                        raise ValidationError("%s 非法值： %s, 参数长度必须大于等于 %s" % (
                            key, len(value), format_data.get(">=")))
                if format_data.get("<=") is not None:
                    if not len(value) <= format_data.get("<="):
                        raise ValidationError("%s 非法值： %s, 参数长度必须小于等于 %s" % (
                            key, len(value), format_data.get("<=")))
                if format_data.get("==") is not None:
                    if not len(value) == format_data.get("=="):
                        raise ValidationError("%s 非法值： %s, 参数长度必须等于 %s" % (
                            key, len(value), format_data.get("==")))
                if "in" in format_data:
                    if value not in format_data.get("in"):
                        raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))

                if "re.match" in format_data:
                    if not re.match(r'%s' % format_data.get("re.match"), value):
                        raise ValidationError("%s 非法值： %s, 不符合规则" % (key, value))

            if format_type == list:
                if "size" in format_data:
                    size_data = format_data.get("size")
                    if size_data.get(">") is not None:
                        le_value = size_data.get(">")
                        for t_value in value:
                            if isinstance(t_value, int):
                                if not t_value > le_value:
                                    raise ValidationError("%s 非法值： %s, 参数值必须大于 %s" % (
                                        key, t_value, le_value))
                            if isinstance(t_value, basestring):
                                if not len(t_value) > le_value:
                                    raise ValidationError("%s 非法值： %s, 参数长度必须大于 %s" % (
                                        key, len(t_value), le_value))
                    if "<" in size_data:
                        le_value = size_data.get("<")
                        for t_value in value:
                            if isinstance(t_value, int):
                                if not t_value < le_value:
                                    raise ValidationError("%s 非法值： %s, 参数值必须小于 %s" % (
                                        key, t_value, le_value))
                            if isinstance(t_value, basestring):
                                if not len(t_value) < le_value:
                                    raise ValidationError("%s 非法值： %s, 参数长度必须小于 %s" % (
                                        key, len(t_value), le_value))
                if "lenth" in format_data:
                    lenth_data = format_data.get("lenth")
                    len_list = len(value)
                    if lenth_data.get(">") is not None:
                        if not len_list > lenth_data.get(">"):
                            raise ValidationError("%s 非法长度：%s 列表长度必须大于 %s" % (
                                key, len_list, lenth_data.get(">")))
                    if "<" in lenth_data:
                        if not len_list < lenth_data.get("<"):
                            raise ValidationError("%s 非法长度：%s 列表长度必须小于 %s" % (
                                key, len_list, lenth_data.get("<")))

                if "in" in format_data:
                    le_value = format_data.get("in")
                    for t_value in value:
                        if t_value not in le_value:
                            raise ValidationError("%s 非法值： %s, 允许的参数值为：%s" % (key, value, format_data.get("in")))

                if "re.match" in format_data:
                    rematch = format_data.get("re.match")
                    for t_value in value:
                        if not re.match(r'%s' % rematch, t_value):
                            raise ValidationError("%s 非法值： %s, 不符合规则" % (key, value))

        if format_data.get("recursive_model"):
            #支持嵌套校验，列表或者字典类型
            if format_type == dict:
                if format_data.get("recursive_model"):
                    recursive_model = format_data["recursive_model"]
                    value = check_params_with_model(value, recursive_model,
                                                    keep_extra_key=keep_extra_key,
                                                    necessary=necessary,
                                                    parent_key=key,
                                                    strip_null_str=strip_null_str
                                                    )
            elif format_type == list:
                temp_list = []
                for v in value:
                    recursive_model = format_data["recursive_model"]
                    v_value = check_params_with_model(v, recursive_model,
                                                      keep_extra_key=keep_extra_key,
                                                      necessary=necessary,
                                                      parent_key=key,
                                                      strip_null_str=strip_null_str
                                                      )
                    temp_list.append(v_value)
                value = temp_list
        return value
    else:
        raise ValidationError("非法类型参数， 参数 %s 传入类型为 %s, 合法类型必须为： %s"
            % (key, _type_to_utf8(type(value)), _type_to_utf8(format_type)))


# --------------------------------


def params_check_with_model(args_dict, model, keep_extra_args=False, strict_mode=False):
    """
    Authored by Jarvis on 2019-05-12.
    :param args_dict: data of dict type that needed to be checked.
    :param model: model for data, which defines data format rules.
    :param keep_extra_args: if keep extra args in result.
    :param strict_mode: if args_dict can have more extra keys than model, which does not exist in model.
    :return:
    """
    if not args_dict:
        return
    if not isinstance(args_dict, dict):
        raise ValidationError("参数结构不合法")
    if not model or not isinstance(model, dict):
        raise ValidationError("参数模型结构不合法")

    pruned_args = {}

    extra_keys = [k for k in args_dict.keys() if k not in model.keys()]

    if strict_mode:
        if extra_keys:
            raise ValidationError("冗余参数")
    else:
        for k in extra_keys:
            v = args_dict.pop(k, None)
            if keep_extra_args:
                pruned_args[k] = v

    for model_k in model.keys():
        model_v = model[model_k]
        arg_v = vv(model_k, model_v, args_dict)
        if arg_v != "NOT__EXIST__IN__MODEL":
            pruned_args[model_k] = arg_v

    return pruned_args


def vv(model_key, model_value, args_dict):
    if model_key not in args_dict:
        if model_value.get("required", False):
            raise ValidationError("缺少必填参数%s" % model_key)
        return "NOT__EXIST__IN__MODEL"

    arg_value = args_dict[model_key]

    if model_value.get("notnull", False):
        if not arg_value and arg_value != 0:
            raise ValidationError("参数%s不能为空" % model_key)
    else:
        if not arg_value:
            return arg_value

    _type = model_value.get("type", None)
    if _type and not isinstance(arg_value, _type):
        raise ValidationError("参数%s类型非法" % model_key)
    _format = model_value.get("format", {})

    if _type is int:
        try:
            arg_value = int(arg_value)
        except Exception as e:
            raise ValidationError("参数%s不是整型" % arg_value)
        check_value_size(model_key, arg_value, arg_value, _format)

    elif _type is float:
        try:
            arg_value = float(arg_value)
        except Exception as e:
            raise ValidationError("参数%s不是浮点型" % arg_value)
        check_value_size(model_key, arg_value, arg_value, _format)

    elif _type is basestring:
        check_value_size(model_key, arg_value, len(arg_value), _format)
        if "re.match" in _format:
            if not re.match(r'%s' % _format.get("re.match"), arg_value):
                raise ValidationError("参数 %s 非法值： %s, 不符合规则" % (model_key, arg_value))

    elif _type is datetime.datetime:
        if isinstance(arg_value, basestring):
            if "/" in arg_value:
                arg_value = arg_value.replace("/", "-")
            arg_value = str_to_time(arg_value)

    elif _type in ("IP", "ip"):
        res, _ = check_ip(arg_value)
        if not res:
            raise ValidationError("参数 %s 值为 %s，不是合法IP地址" % (model_key, arg_value))

    elif _type in ("email", "e-mail", "Email", "E-mail"):
        res = check_email_address(arg_value)
        if not res:
            raise ValidationError("参数 %s 值为 %s，不是合法的e-mail地址" % (model_key, arg_value))

    elif _type in (list, tuple, set):
        _all_elements_formats = _format.get("element_format", {})
        for arg_item_value in arg_value:
            vv(model_key, _all_elements_formats, {model_key: arg_item_value})

    elif _type is dict:
        _all_elements_formats = _format.get("element_format", {})
        # for k in arg_value:   # arg_value is a dict now.
        for k in _all_elements_formats.keys():
            vv(k, _all_elements_formats.get(k, {}), arg_value)

    else:
        raise ValidationError("暂不支持的参数类型")

    return arg_value


def check_value_size(key, value, value_size, referred_value):
    if not isinstance(referred_value, dict):
        raise ValueError("model格式错误")
    desc = {
        "lt": "小于",
        "le": "小于或等于",
        "gt": "大于",
        "gte": "大于或等于",
        "in": "符合范围"
    }

    err_flag = False
    operator = None
    origin_operator = None
    for k in referred_value:
        if k in ("lt", "<"):
            if value_size >= referred_value[k]:
                err_flag = True
                operator = "lt"
                origin_operator = k
                break
        elif k in ("le", "lte", "<="):
            if value_size > referred_value[k]:
                err_flag = True
                operator = "le"
                origin_operator = k
                break
        elif k in ("gt", ">"):
            if value_size <= referred_value[k]:
                err_flag = True
                operator = "gt"
                origin_operator = k
                break
        elif k in ("gte", ">="):
            if value_size < referred_value[k]:
                err_flag = True
                operator = "gte"
                origin_operator = k
                break
        elif k == "in":
            if value not in referred_value[k]:
                err_flag = True
                operator = "in"
                origin_operator = k
                break
        else:
            return

    if err_flag:
        raise ValidationError("参数{0}超出限制，必须{1}{2}".format(key, desc[operator], referred_value[origin_operator]))


if __name__ == '__main__':
    adb = {
        "id": {"type": int, "notnull": False, "format": {">": 0, "<": 255, "in": [1, 2, 3, 4]}},
        "name": {"type": basestring, "required": False, "notnull": True, "format": {">": 2, "<": 255, "re.match":"[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[comnet]{1,3}$"}},
        "desc": {"type": datetime.datetime},
        "status": {"type": bool, "required": False},
        "ss": {"type": list, "notnull": False},
        "ggg": {"type": dict},
        "xxx": {"type": "ip"},
        "xcss": {"type": "email"},
        "testfloat": {"required": True, "type": float, "notnull": True, "format": {">": 100, "<": 200}},
        "testint": {"type": int, "notnull": True},
        "teststr": {"type": basestring, "notnull": True, "required": True},
        "test_dict": {
            "type": dict,
            "notnull": True,
            "format": {
                "element_format": {
                    "aa": {"type": basestring, "notnull": True, "required": True, "format": {"lt": 3, ">": 0}},
                    "bb": {
                        "type": dict,
                        "notnull": True,
                        "format": {
                            "element_format": {
                                "cc": {
                                    "type": tuple,
                                    "notnull": True,
                                    "required": True,
                                    "format": {
                                        "element_format": {
                                            "type": basestring,
                                            "notnull": True,
                                            "required": True,
                                            "format": {"lt": 3, ">": 0}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "test_list_0": {
            "type": list,
            "notnull": True,
            "format": {
                "element_format": {
                    "type": basestring, "notnull": True, "required": True, "format": {"lt": 3, ">": 0}
                }
            }
        }
    }
    data = {
        "id": None,
        # "name": "fff",
        "desc": "2000/01/08",
        # "ss": None,
        "xxx": "192.168.137.255",
        "ggg": {},
        "xcss": "a@cmrh.com",
        "testfloat": 111,
        "testint": 1,
        "teststr": "123",
        "test_dict": {"aa": "jj", "bb": {"cc": ["ddd"]}},
        "test_list_0": ["aa", "bb"]
    }
    # gsss = check_params_with_model(data, adb)
    gsss = params_check_with_model(data, adb)
    print(gsss)
