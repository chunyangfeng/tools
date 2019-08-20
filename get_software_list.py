#!/usr/bin/env python
# coding:utf-8

"""
Author: 冯春阳
Date: 2018/07/10
"""

import _winreg
import time
import xlwt


sub_key = [
    r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
    r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
]  # 需要遍历的两个注册表

software_list = []

for i in sub_key:
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, i, 0)
    for j in range(0, _winreg.QueryInfoKey(key)[0] - 1):
        try:
            key_name = _winreg.EnumKey(key, j)
            key_path = i + '\\' + key_name
            each_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key_path, 0)
            DisplayVersion, _ = _winreg.QueryValueEx(each_key, 'DisplayVersion')
            DisplayName, _ = _winreg.QueryValueEx(each_key, 'DisplayName')
            software_list.append((DisplayName, DisplayVersion))
        except WindowsError:
            pass

software_list = sorted(list(set(software_list)))  # 去重排序

w_book = xlwt.Workbook()
sheet = w_book.add_sheet("result")

line = len(software_list) - 1  # 获取excel行索引编号

for name, version in software_list:
    sheet.write(line, 0, name)
    sheet.write(line, 1, version)
    line -= 1

w_book.save("result.xls")

print u"软件安装列表采集完毕，请查看当前目录下的result.xls文件"


time.sleep(1)

