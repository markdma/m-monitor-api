# coding: utf-8
import datetime
import time


def datetime_str_to_timestamp(datetime_str, format, is_float=False):
    the_datetime = datetime.datetime.strptime(datetime_str, format)
    return datetime_to_timestamp(the_datetime, is_float)


def datetime_to_timestamp(the_datetime, is_float=False):
    '''
        datetime类型成为时间戳
    :param the_datetime:
    :return int / float:
    '''
    ms = time.mktime(the_datetime.timetuple())
    if not is_float:
        ms = int(ms)
    return ms


def str_to_time(date_str):
    if ":" in date_str:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')


def timestamp_to_date_str(ts):
    '''
        timestamp 转日期字符串
    :param ts:
    :return:
    '''
    try:
        time_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    except:
        time_str = ""
    return time_str


def get_timestamp(time_str):
    """
    string类型的时间，返回时间戳格式
    :param time_str:
    :return:
    """
    try:
        if ":" in time_str:
            start_time_timestamp = datetime_str_to_timestamp(time_str, '%Y-%m-%d %H:%M:%S')
        else:
            start_time_timestamp = datetime_str_to_timestamp(time_str, '%Y-%m-%d')
    except Exception as e:
        raise Exception("非法的时间格式")
    return start_time_timestamp


def get_timestamp_now():
    return time.time()


def get_yesterday_str():
    yesterday = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), '%Y-%m-%d') + datetime.timedelta(days=-1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    return yesterday_str


def is_data_str(time_str):
    """
    string类型的时间，返回True or Exception
    :param time_str:
    :return:
    """
    try:
        _ = datetime_str_to_timestamp(time_str, '%Y-%m-%d')
    except Exception as e:
        raise Exception("非法的时间格式")
    return True


def get_now_str(format_str=""):
    """
    获取当前时间字符串 '2021-08-18'
    :return: str
    """
    try:
        if format_str:
            return time.strftime(format_str)
        else:
            return time.strftime("%Y-%m-%d")
    except Exception as e:
        return ""

