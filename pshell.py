#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import paramiko
import getpass
from time import sleep


def pshell():
    hostname = raw_input("Input hostname or ip address:")
    port = raw_input("Input remote port:")
    username = raw_input("Input remote username:")
    password = getpass.getpass("Input remote password:")
    trans = paramiko.Transport(sock=(hostname, int(port)), )
    try:
        trans.connect(username=username, password=password)
        ssh = paramiko.SSHClient()
        ssh._transport = trans
        cmd_line = r"[%s@%s]>>>".replace(r"'", "") % (username, hostname)
        usage = """Common command:\nexit:Logout the ssh session;\nhelp:Display help information."""
        print cmd_line + "\n" + usage
        flag = True
        while flag:
            command = raw_input(cmd_line)
            if command.lower() == "exit":
                flag = False
                trans.close()
                print cmd_line + "Logout the ssh session."
            elif command.lower() == "help":
                print usage
            else:
                stdin, stdout, stderr = ssh.exec_command(command)
                error = stderr.read()
                output = stdout.read()
                if error:
                    print error
                else:
                    print output
    except paramiko.AuthenticationException, e:
        print e
        sleep(3)
    return pshell()


if __name__ == "__main__":
    pshell()
