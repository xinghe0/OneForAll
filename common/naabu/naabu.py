# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/2 4:51 PM
@Auth ： xinghe
@File ：naabu.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""
import os
import concurrent.futures
import requests
import xml.etree.ElementTree as ET
from config.log import logger

requests.packages.urllib3.disable_warnings()  # 屏蔽ssl报错


def naabu_cmd(path, nmap):
    if nmap:
        paths = str(path).split('.')[0]
        # common/naabu/naabu
        command = f'common/naabu/naabu -list {path} -top-ports 100 -nmap-cli \'nmap -sV -oX {paths}_nmap-output.xml\' -o {paths}_result.txt'
        os.system(command)
        check_http_services(f'{paths}_nmap-output.xml')
    else:
        paths = str(path).split('.')[0]
        command = f'common/naabu/naabu -list {path} -top-ports 1000 -o {paths}_result.txt'
        os.system(command)
        sub_list = []
        for i in open(f'{paths}_result.txt','r'):
            sub_list.append(i)

        result = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(check_single_url, f"{address}:{portid}") for (address, portid) in sub_list]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res is not None:
                    result.append(res)

        # 将结果写入到同名的 TXT 文件中
        with open(path.rsplit('.', 1)[0] + '_web.txt', 'w') as f:
            for url in result:
                url = str(url).split('//')[1]
                f.write(url + '\n')



def check_single_url(url: str, timeout: float = 3):
    # 尝试以 http 和 https 协议访问该 URL，如果能够成功，就返回该 URL
    http_list = ['http://', 'https://']
    for protocol in http_list:
        try:
            result = requests.get(protocol + url, timeout=timeout)
            if result.status_code in range(200, 500):
                return protocol + url
        except Exception as e:
            pass


def check_http_services(path: str, max_workers: int = 20):
    # 解析 XML 文件并获取所有需要进行检测的主机端口信息
    tree = ET.parse(path)
    root = tree.getroot()
    targets = []
    for host in root.findall('host'):
        address = host.find('address').get('addr')
        for port in host.findall('ports/port'):
            portid = port.get('portid')
            state_state = port.find('state').get('state')
            if state_state == "open":
                targets.append((address, portid))
            else:
                pass
    # 使用多线程检测每个目标的可访问性
    result = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_single_url, f"{address}:{portid}") for (address, portid) in targets]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is not None:
                result.append(res)

    # 将结果写入到同名的 TXT 文件中
    with open(path.rsplit('.', 1)[0] + '_web.txt', 'w') as f:
        for url in result:
            url = str(url).split('//')[1]
            f.write(url + '\n')
