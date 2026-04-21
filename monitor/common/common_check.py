# coding: utf-8
import re


class UserCheck(object):

    def validate_phone(self, phone):
        """
        检测手机号码的国家码,暂时支持大陆/香港/台湾/澳门/新加坡
        :param phone:
        :return:  是否为上述地区的手机号码/格式化后的手机号码/国家码
        """
        CHINA_CODE = "86"
        HONGKONG_CODE = "852"
        MACAO_CODE = "853"
        TAIWAN_CODE = "886"
        SINGAPORE = "65"

        if phone:
            # 大陆手机号11位，区号是86
            if re.match(
                r'^([+]?((0)?|(00)?)(86)?[-]?)(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$',
                    phone):
                return True, phone[-11:], CHINA_CODE
            # 香港手机号8位，区号是852
            if re.match(r'^([+]?((0)?|(00)?)(852)?[-]?)(5|6|8|9)\d{7}$', phone):
                return True, phone[-8:], HONGKONG_CODE
            # 澳门手机号7位，区号是853
            if re.match(r'^([+]?((0)?|(00)?)(853)?[-]?)[6]([8|6])\d{5}$', phone):
                return True, phone[-7:], MACAO_CODE
            # 台湾手机号10位，区号是886
            if re.match(r'^([+]?((0)?|(00)?)(886)?[-]?)[0][9]\d{8}$', phone):
                return True, phone[-10:], TAIWAN_CODE
            # 新加坡手机号8位，区号是65
            if re.match(r'^([+]?((0)?|(00)?|(000)?)(65)?[-]?)(8|9)\d{7}$', phone):
                return True, phone[-8:], SINGAPORE
        return False, phone, None