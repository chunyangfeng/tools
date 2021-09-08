"""
Date: 2021/9/8 11:44

Author: Fengchunyang

Record:
    2021/9/8 Create file.

"""
import os
import subprocess


class ShellExecutor:
    def __init__(self):
        pass

    @staticmethod
    def exec_by_os(command):
        """使用os.system方法调用shell命令，返回值为shell执行后的状态码，0表示执行成功，其他表示执行失败
        此方法适用于shell命令不需要输出内容的场景

        Args:
            command(str): shell命令

        Returns:
            code(int): 执行状态码
        """
        code = os.system(command)
        return code

    @staticmethod
    def exec_by_subprocess(command):
        """使用subprocess调用shell命令，可以获取到执行结果、执行错误、执行状态码

        Args:
            command(str): shell命令

        Returns:
            code(int): 执行状态码
            stdout(str): 输出内容
            stderr(str): 输出错误
        """
        popen = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = popen.communicate(timeout=10)
        code = popen.returncode
        return code, stdout, stderr
