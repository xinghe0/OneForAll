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

def naabu_cmd(path):
    paths = str(path).split('.')[0]
    #common/naabu/naabu
    command = f'./naabu -list {path} -top-ports 100 -nmap-cli \'nmap -sV -oX {paths}_nmap-output.xml\' -o {paths}_result.txt'
    os.system(command)


def info(path):
    tree = ET.parse(path)
    root = tree.getroot()
    result = []

    # 遍历每个host节点，获取地址、端口和服务名称信息
    for host in root.findall('host'):
        address = host.find('address').get('addr')
        for port in host.findall('ports/port'):
            portid = port.get('portid')
            service_name = port.find('service').get('name')
            product_name = port.find('service').get('product')
            result.append(f'{address}:{portid}')
    print(result)
    return result


if __name__ == '__main__':
    path = 'url.txt'
    naabu_cmd(path)
    info(f'{path.split(".")[0]}_nmap-output.xml')