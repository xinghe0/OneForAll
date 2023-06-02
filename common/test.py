# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/2 10:39 AM
@Auth ： xinghe
@File ：Oneforall_api.py.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""
import json
import ipaddress

def nginx_ip(data):
    result = []
    json_obj = json.loads(data)
    for obj in json_obj:
        if obj['banner'] == 'nginx':
            result.append(obj['ip'])
    result = set(result)
    new_list = list(result)
    new_lists = []
    for item in new_list:
        new_lists.extend(item.split(','))
    return new_lists


def intranet_host(data):
    result = []
    json_obj = json.loads(data)
    for obj in json_obj:
        if ',' in str(obj['ip']):
            for i in str(obj['ip']).split(','):
                if is_private_ip(i) and i != '127.0.0.1':
                    result.append(obj['subdomain'])
        else:
            if is_private_ip(obj['ip']) and obj['ip'] != '127.0.0.1':
                result.append(obj['subdomain'])
    result = list(set(result))
    return result





def is_private_ip(ip):
    """
    判断是否为内网IP地址
    :param ip: IP地址字符串，如'192.168.1.1'
    :return: True或False
    """
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private
    except ValueError:
        return False



data = open('../results/douyu.com.json','r')
data = data.read()
nginx_ip(data)
intranet_host(data)

