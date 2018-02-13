#! /usr/local/bin python3.6
"""
@Time    : 2018/2/13 12:23
@Author  : ysj
@Site    : 
@File    : port_check.py
@Software: PyCharm
"""

import socket


def port_check(ip, port=None):
    if ip and ':' in ip:
        ip, port = ip.strip().split(':')
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # noinspection PyBroadException
    try:
        sk.settimeout(1)
        sk.connect((ip, int(port)))
        return True
    except Exception:
        return
    sk.close()


if __name__ == '__main__':
    port_check('smtp.qq.com:25')