# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/5 3:26 PM
@Auth ： xinghe
@File ：call.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""
import os
import xml.etree.ElementTree as ET
import requests


def naabu_cmd(path):
    paths = str(path).split('.')[0]
    #common/naabu/naabu
    command = f'./naabu -list {path} -top-ports 100 -nmap-cli \'nmap -sV -oX {paths}_nmap-output.xml\' -o {paths}_result.txt'
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
            state_state = port.find('state').get('state')
            product_name = port.find('service').get('product')
            print(f'{address}:{portid},status:{state_state}')
            if service_name == "http" and state_state == "open":
                print(f'This is http: {address}:{portid},status:{state_state}')
                result.append(f'{address}:{portid}')
            else:
                fit.append(f'{address}:{portid}')
                http_live = http(fit)
                if http_live:
                    result.append(http(fit))
    print(result)
    for i in result:
        with open(str(path).split('.')[0] + '.txt','a+') as f:
            f.write(i + '\n')
            f.close()
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





info('../../results/all_subdomain_result_20230605_142102_nmap-output.xml')