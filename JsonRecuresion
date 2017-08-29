#!/usr/bin/env python
# coding:utf-8

import json

class JsonRecursion:
    """
    处理json数据的类。可以将json数据转换成纯字典的格式，其中字典的key将按照原字典key的深度，按照递归切割符连接组合成新key。
    """
    def __init__(self, file_path=None, json_data=None):
        self.file_path = file_path
        self.json_data = json_data
        self.result = {}
        self.dicts = {}

    def json_to_dict(self, fp):
        try:
            with open(fp, "r") as f:
                json_dict = json.loads(f.readlines()[0])
        except:
            print u"请输入正确的json文件路径"
            json_dict = {}
        return json_dict

    def data_resolve(self, data_dict, flag=True, split_flag=r"/"):
        """
        接收一个数据类型的原始字典，同时通过标志位来判断程序的处理流程，最后将结果以递归切割符作连接，替换原始字典。
        :param data_dict:一个数据类型为字典的参数，是处理的原始数据；
        :param flag:标志位。标志位=True的含义为传过来的参数字典中存在以字典作为value的情况；
                    当标志位为False时，则代表递归结束，即flag=False为递归的出口；
        :param split_flag:递归深度切割符，默认为“/；
        :return:返回一个字典。
        """
        data = data_dict  # 将传递过来的字典重新赋值给data标量
        if flag:  # 判断标志位是否为真，如果为真，将继续执行递归，如果为假，则返回data
            flag_list = []  # 标志位列表，用于判断递归是否继续进行
            for k, v in data.items():  # 第一轮迭代，获取data中的key和value
                if isinstance(v, dict):  # 判断第一轮迭代出来的value是否有字典
                    for k1, v1 in v.items():  # 第二轮迭代，迭代该子字典中的key和value
                        data[str(k) + split_flag + str(k1)] = v1  # 将本次第一轮迭代出来key加上递归切割符，再加上第二轮迭代出来的
                        # key作为新key，同时将第二轮迭代出来的value重新赋值给新key
                    data.pop(k)  # 删除本次第一轮迭代中value为字典的key
                    flag_list.append(True)  # 向标志位列表中追加一次value是字典的标识，True
                elif isinstance(v, list):  # 如果第一轮迭代出来的value不是字典，是列表，则进行对列表的处理
                    for index in range(len(v)):  # 第二轮迭代，获取value为列表的所有索引
                        data[str(k) + split_flag + str(index)] = v[index]  # 将第一轮迭代的key加上递归切割符，再加上第二轮迭代的
                        # 索引值作为新key，同时将获取第一轮迭代出的列表的该索引对应的值重新赋值给新key。
                    data.pop(k)  # 删除本次第一轮迭代中value为列表的key
                    flag_list.append(True)  # 向标志位列表中追加一次value是列表的标识，True
                flag_list.append(False)  # 如果第一轮迭代中没有字典也没有列表，则向标志位列表中追加一个False
            for flag in flag_list:  # 第一轮迭代结束后，判断标志位列表中是否存在flag=True的标志位，如果存在，说明本轮递归中，还存在value
                # 为字典或者列表的情况，递归将继续，如果标志位列表中全部都是False，则说明本轮递归中，所有的value都不存在为字典或者列表的情况，递归结束，返回最终的结果data
                if flag:
                    return self.data_resolve(data_dict=data, flag=flag)
                pass
        return data

    def main(self, fp, split_flag=r"/"):
        """
        主函数，用于执行一次完整的json数据处理。
        :param fp:一个json数据文件的绝对路径；
        :param split_flag:递归深度切割符，默认为“/；
        :return: 返回结果为一个字典。
        """
        json_data = self.json_to_dict(fp)
        recursion_data = self.data_resolve(data_dict=json_data,split_flag=split_flag)
        return recursion_data
