import ipaddress

from monitor.core.utils import ensure_unicode


def ipv6_validator(ip):
    try:
        ipaddress.IPv6Address(ensure_unicode(str(ip)))
        return True
    except Exception as e:
        return False