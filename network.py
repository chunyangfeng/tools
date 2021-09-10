# -*- coding: utf-8 -*-
"""网络相关工具
时间: 2020/12/5 11:10

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/5 新增文件。

重要说明:
"""
import re
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
    """使用request发起http请求
        res.encoding                # 获取当前的编码
        res.encoding = 'utf-8'      # 设置编码
        res.text                    # 以encoding解析返回内容。字符串方式的响应体，会自动根据响应头部的字符编码进行解码。
        res.content                 # 以字节形式（二进制）返回。字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩。
        res.headers                 # 以字典对象存储服务器响应头，但是这个字典比较特殊，字典键不区分大小写，若键不存在则返回None
        res.status_code             # 响应状态码
        res.raw                     # 返回原始响应体，也就是 urllib 的 response 对象，使用 r.raw.read()
        res.ok                      # 查看r.ok的布尔值便可以知道是否登陆成功
        res.json()                  # Requests中内置的JSON解码器，以json形式返回
        res.raise_for_status()      # 失败请求(非200响应)抛出异常
    """
    def __init__(self):
        self._header = self._get_header()
        self._timeout = 5

    @staticmethod
    def _get_header():
        """构造默认header字典

        Returns:
            header(dict): header字典
        """
        header = {
            'Content-Type': 'application/json'
        }
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
            response = requests.get(url, params=params, headers=self._header, timeout=self._timeout)
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
            response = requests.post(url, data=data, headers=self._header, timeout=self._timeout)
        except RequestException:
            return 0, None, "Connect Failed"
        return response.status_code, response, "Success"

    def put(self, url, params, data, header=None):
        """发起put请求

        Args:
            url(str): 请求地址
            params(dist): 请求参数
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
            response = requests.put(url, params=params, data=data, headers=self._header, timeout=self._timeout)
        except RequestException:
            return 0, None, "Connect Failed"
        return response.status_code, response, "Success"

    def delete(self, url, params, data, header=None):
        """发起delete请求

        Args:
            url(str): 请求地址
            params(dist): 请求参数
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
            response = requests.delete(url, params=params, data=data, headers=self._header, timeout=self._timeout)
        except RequestException:
            return 0, None, "Connect Failed"
        return response.status_code, response, "Success"


def is_legal_ip(ipaddr):
    """判断给定的ip地址是否合法

    Args:
        ipaddr(str): 待检验的ip地址，需满足点分十进制的表示法

    Returns:
        is_legal(bool): 是否合法
    """
    cmp = re.compile(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    result = cmp.match(ipaddr)
    return True if result else False


