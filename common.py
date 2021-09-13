#!/usr/bin/env python
# coding:utf-8
# Author:Fengchunyang
"""
通用功能函数
"""
import json
import datetime
import base64
import hashlib
import socket
import sys
import os
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from collections import OrderedDict, defaultdict


def strftime(obj, formatter="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strftime(obj, formatter) if obj else obj


def strptime(s, formatter="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(s, formatter) if s else s


def num_to_str(number):
    mapping = {
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "日"
    }
    return mapping.get(str(number))


def data_diff(put_data, instance):
    diff = "实例ID{0}变更记录为:".format(instance[0].id)
    if instance:
        for k, v in put_data.items():
            try:
                db_data = eval("instance[0].{0}".format(k))
                if v != db_data:
                    diff += "{0}:[{1}-->{2}],".format(k, db_data, v)
            except AttributeError:
                pass
    return diff


class AesHandler:
    def __init__(self):
        self._salt = "qBfLtQIbZfZgVJvTuTDMEq46tMinYpQX"
        self._key = base64.b64decode(self._salt)
        self._iv = b'0000000000000000'
        self._mode = AES.new(self._key, AES.MODE_CBC, self._iv)
        self._block_size = 32

    def fill_text(self, text):
        """文本长度不足位的，补充空格至最大位数"""
        if len(text) < self._block_size:
            text += '\0' * (self._block_size - len(text))
        return text.encode("utf-8")

    def encrypt(self, text):
        """加密文本"""
        text = self.fill_text(text)
        mode = AES.new(self._key, AES.MODE_CBC, self._iv)
        cipher_text = mode.encrypt(text)
        return b2a_hex(cipher_text)

    def decrypt(self, text):
        """解密文本"""
        mode = AES.new(self._key, AES.MODE_CBC, self._iv)
        plain_text = mode.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip("\0")


def get_md5(obj):
    """
    获取传入的不可变对象的md5
    :param obj: 不可变的对象
    :return: md5
    """
    md5 = hashlib.md5()
    md5.update(obj.encode("utf8"))
    return md5.hexdigest()


def get_two_week():
    """
    获取包含当前日期所在的两周起始日期，起点为距离当前天最近的上一个周一，终点为距离起点两周后的周五
    :return:  [start_date, end_date]
    """
    now = datetime.datetime.now().date()
    start_date = now - datetime.timedelta(days=now.isoweekday()+6)
    end_date = start_date + datetime.timedelta(days=18)
    return start_date, end_date


def get_two_week_inspect():
    """
    获取包含当前日期所在的两周起始日期，起点为距离当前天最近的上一个周一，终点为距离起点两周后的周五
    :return:  [start_date, end_date]
    """
    now = datetime.datetime.now().date()
    start_date = now - datetime.timedelta(days=now.isoweekday()+6)
    end_date = start_date + datetime.timedelta(days=13)
    return start_date, end_date


def get_last_week(date=None):
    """
    获取指定日期的上一周的起始日期，默认为当前日期
    :param date: 指定日期对象或日期字符串，默认为当前日期
    :return: 列表，值为[上周一日期，上周日日期]
    """
    if date is None:
        date = datetime.datetime.now().date()
    else:
        if isinstance(date, str):
            date = strptime(date, "%Y-%m-%d")
    start = date - datetime.timedelta(days=date.isoweekday()+6)
    end = date - datetime.timedelta(days=date.isoweekday())
    return start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d") + " 23:59:59"


def ip_connect_check(ip, port):
    """
    根据给定的IP和端口判断与目标接口的连通性
    :param ip: 符合点分十进制规则的IP地址或者域名
    :param port: 端口号
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False


def continued(date_start, date_end=None):
    """
    判断两个给定日期字符串的时间差
    :param date_start: 开始日期datetime对象或日期字符串，eg：'2020-04-01 17:00:00'
    :param date_end: 结束日期datetime对象或日期字符串，eg：'2020-04-01-18:00:00',默认使用当前时间
    :return: 时间差描述字符串，形如'3天12小时35分钟40秒'
    """
    mapping = OrderedDict()
    mapping["天"] = 24*60*60
    mapping["小时"] = 60*60
    mapping["分钟"] = 60
    if date_end is None:
        date_end = datetime.datetime.now()
    else:
        if isinstance(date_end, str):
            date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")
    if isinstance(date_start, str):
        date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")
    timedelta = date_end - date_start if date_end >= date_start else date_start - date_end
    seconds = int(timedelta.total_seconds())
    result = ""
    for k, v in mapping.items():
        r = int(seconds / v)
        if r >= 1:
            result += "{0}{1}".format(r, k)
            seconds -= r*v
    return result










