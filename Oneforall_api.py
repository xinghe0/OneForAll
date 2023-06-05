#!/usr/bin/env python3
# coding=utf-8

"""
Example
"""

from oneforall import OneForAll
from common.naabu.naabu import naabu_cmd

def oneforall(file):
    """
    oneforall子域名接口扫描api
    :param domain:
    :return:
    """
    test = OneForAll(targets=file)
    test.dns = True
    test.brute = True
    test.req = True
    test.takeover = False
    test.run()

if __name__ == '__main__':
    oneforall('url.txt')
