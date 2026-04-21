# coding: utf-8
import random
import string
import time


class RandomUtil(object):
    def __init__(self):
        self.str = ''
        self.time_now = ''

    def random_str(self, str_length, no_length=0, start_with='', end_with='', lower_upper_flag=0, date_time_flag=False):
        """
        随机生成字符串
        :param str_length: 指定随机生成字符串的长度
        :param no_length: 指定随机生成的字符串中数值的长度
        :param start_with: 指定随机字符串的开头
        :param end_with: 指定随机字符串的结尾
        :param lower_upper_flag: 指定生成大小写字母,1为小写,2为大写,其他均不处理
        :param date_time_flag: 指定是否生成当前时间
        :return:
        """
        if str_length > 0:
            self.str = ''.join([random.choice(string.ascii_letters) for x in range(int(str_length))])
            if lower_upper_flag == 1:
                self.str = self.str.lower()
            elif lower_upper_flag == 2:
                self.str = self.str.upper()
        if no_length > 0:
            self.str = self.str + ''.join([random.choice(string.digits) for x in range(no_length)])
        if date_time_flag:
            self.time_now = time.strftime('%Y-%m-%d %H:%M:%S')
        return start_with + self.str + end_with + self.time_now