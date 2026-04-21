import IPy


class IPv6FilerConvert:
    @staticmethod
    def ipv6_filter_convert(filed, filed_filter=None):
        if filed_filter:
            ipv6_address_filter = filed_filter.get(filed, None)
            if ipv6_address_filter:
                if isinstance(ipv6_address_filter, dict):
                    for key in ipv6_address_filter.keys():
                        value = ipv6_address_filter[key]
                        if isinstance(value, str):
                            ipv6_address_filter[key] = IPv6FilerConvert.ipv6_simple(ipv6_address_filter[key])
                elif isinstance(ipv6_address_filter, str):
                    filed_filter[filed] = IPv6FilerConvert.ipv6_simple(ipv6_address_filter)

    @staticmethod
    def ipv6_simple(ipv6):
        try:
            ip = IPy.IP(ipv6)
            if ip.version() == 6:
                return str(ip)
            return ipv6
        except Exception:
            return ipv6
