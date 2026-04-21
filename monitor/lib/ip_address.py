# coding=utf-8
# author='rd'

from __future__ import absolute_import

import IPy
from monitor.core.exceptions import ValidationError

# def check_ip(ip):
#     if ip:
#         if not len(ip.split("/")) == 1:
#             return False, "%s is invalid" % ip
#         else:
#             try:
#                 IPy.IP(ip).strNormal()
#                 return True, "ok"
#             except Exception, e:
#                 return False, e
#     else:
#         return False, "ip is null"

def check_ip(ip):
    try:
        if ip.strip():
            if not len(ip.split("/")) == 1:
                return False, "非法的ip: %s" % ip
            else:
                try:
                    t_res = ip.split(".")
                    if len(t_res) != 4:
                        raise ValidationError("非法的ip: %s" % ip)
                    IPy.IP(ip).strNormal()
                    return True, "ok"
                except Exception, e:
                    return False, e
        else:
            return False, "ip 为空"
    except Exception, e:
        raise ValidationError("非法的ip: %s" % ip)


def check_ips(ip_list):
    if not isinstance(ip_list, (list, basestring)):
        return False, "must give ip list or str with , split"

    if isinstance(ip_list, basestring):
        if ip_list.strip():
            ip_list = ip_list.split(",")
        else:
            raise ValidationError("ip 为空")

    failed_list = []
    failed_lenth = 0
    for ip in ip_list:
        status, result = check_ip(ip)
        if not status:
            failed_lenth += 1
            failed_list.append(ip)

    if failed_lenth:
        return False, "非法的ip列表：%s" % failed_list
    else:
        return True, "ok"
