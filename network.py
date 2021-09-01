# -*- coding: utf-8 -*-
"""网络相关工具
时间: 2020/12/5 11:10

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/5 新增文件。

重要说明:
"""
import requests
import socket
from requests.exceptions import RequestException


def ip_connect_check(fqdn, port):
    """
    根据给定的IP和端口判断与目标接口的连通性
    :param fqdn: 符合点分十进制规则的IP地址或者域名
    :param port: 端口号
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((fqdn, int(port)))
    return result == 0


def get_ip_info(ipaddr):
    """获取IP地址相关信息

    Args:
        ipaddr(str): ip地址

    Returns:
        data(dict): IP地址相关信息
    """
    ip_info_api = "http://ip-api.com/json/"
    url = f'{ip_info_api}/{ipaddr}?lang=zh-CN'
    try:
        response = requests.get(url)
    except RequestException:
        return dict()
    return response.json() if response.status_code == 200 else dict()


def baidu_api_put(site, token, data):
    """Baidu 收录推送

    Args:
        site(str): 推送网站
        token(str): 网站token
        data(list): 推送地址列表

    Returns:
        result(dict): 结果
    """
    headers = {
        'Host': 'data.zz.baidu.com',
        'Content - Type': 'text/plain',
    }
    baidu_seo_api = "http://data.zz.baidu.com/urls"
    api = f'{baidu_seo_api}?site={site}&token={token}'
    try:
        response = requests.post(api, headers=headers, data='\n'.join(data), timeout=5)
    except Exception as e:
        return '400', e
    return response.status_code, response.json()


class RequestResolve:
    """使用request发起http请求"""
    def __init__(self):
        self._header = self._get_header()

    @staticmethod
    def _get_header():
        """构造默认header字典

        Returns:
            header(dict): header字典
        """
        header = dict()
        return header

    def _update_header(self, header):
        """覆盖更新默认header配置字典

        Args:
            header(dict): 需要更新的header字典
        """
        for key, value in header.items():
            self._header[key] = value

    def get(self, url, params=None, header=None):
        """发起get请求

        Args:
            url(str): 请求地址
            params(dict|None): 查询字符串，传参结构为字典
            header(dict|None): 指定特殊的header，该参数如果被指定，则会覆盖更新默认header

        Returns:
            code(int): 状态码，如果返回状态码0则代表访问失败
            response(any): 响应数据
            msg(str): 请求结果
        """
        if header is not None:
            self._update_header(header)
        try:
            response = requests.get(url, params=params, headers=self._header)
        except RequestException:
            return 0, None, "Connect Failed"
        return response.status_code, response, "Success"

    def post(self, url, data, header=None):
        """发起post请求

        Args:
            url(str): 请求地址
            data(dict): post请求发送的数据
            header(dict|None): 特殊指定header

        Returns:
            code(int): 状态码，如果返回状态码0则代表访问失败
            response(any): 响应数据
            msg(str): 请求结果
        """
        if header is not None:
            self._update_header(header)
        try:
            response = requests.post(url, data=data, headers=self._header)
        except RequestException:
            return 0, None, "Connect Failed"
        return response.status_code, response, "Success"


