# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/2 4:51 PM
@Auth ： xinghe
@File ：naabu.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""
import os
import xml.etree.ElementTree as ET
import requests
from config.log import logger

requests.packages.urllib3.disable_warnings()  # 屏蔽ssl报错

def naabu_cmd(path):
    paths = str(path).split('.')[0]
    #common/naabu/naabu
    command = f'common/naabu/naabu -list {path} -top-ports 100 -nmap-cli \'nmap -sV -oX {paths}_nmap-output.xml\' -o {paths}_result.txt'
    os.system(command)
    info(f'{paths}_nmap-output.xml')


def info(path):
    tree = ET.parse(path)
    root = tree.getroot()
    result = []
    fit = []

    # 遍历每个host节点，获取地址、端口和服务名称信息
    for host in root.findall('host'):
        address = host.find('address').get('addr')
        for port in host.findall('ports/port'):
            portid = port.get('portid')
            service_name = port.find('service').get('name')
            product_name = port.find('service').get('product')
            if service_name == "http":
                result.append(f'{address}:{portid}')
            else:
                fit.append(f'{address}:{portid}')
                http_live = http(fit)
                if http_live:
                    result.append(http(fit))
    logger.log("INFOR",f'Http server list: {result}')
    return result

def http(url_list):
    http_list = ['http://','https://']
    for i in http_list:
        for j in url_list:
            try:
                result = requests.get(url=i + j,timeout=3)
                if result.status_code in range(600):
                    return j
            except Exception as e:
                pass


if __name__ == '__main__':
    path = 'url.txt'
    naabu_cmd(path)
    info(f'{path.split(".")[0]}_nmap-output.xml')