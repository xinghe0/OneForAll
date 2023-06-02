#!/usr/bin/env python3
# coding=utf-8

"""
Example
"""

from oneforall import OneForAll


def oneforall(file):
    """
    sdsd
    :param domain:
    :return:
    """
    test = OneForAll(targets=file)
    test.dns = True
    test.brute = False
    test.req = True
    test.takeover = False
    test.run()
    results = test.datas

    print(f'{type(results)}')


if __name__ == '__main__':
    oneforall('url.txt')
