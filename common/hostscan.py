# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/2 2:40 PM
@Auth ： xinghe
@File ：hostscan.py
@IDE ：PyCharm
@Motto:但行好事，莫问前程
"""
import threading
import re, queue, requests, time

queues = queue.Queue()
info_queue = queue.Queue()
threadLock = threading.Lock()
requests.packages.urllib3.disable_warnings()  # 屏蔽ssl报错
threads_complete = True
queues_size = 0  # 存放总的数量
now_size = 0  # 现在进度
switch = 1  # 开关


class get_therad(threading.Thread):  # 网络请求线程
    def __init__(self, url_ip, name):
        threading.Thread.__init__(self)
        self.url_ip = url_ip
        self.name = name

    def run(self):
        threadLock.acquire()
        threadLock.release()
        while not self.url_ip.empty():
            url_ips = self.url_ip.get()
            for i in ['http://', 'https://']:
                url = i + url_ips[1]
                host = url_ips[0]
                headers = {
                    'host': '%s' % (host),
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                    'Referer': 'http://www.baidu.com',
                    'Connection': 'close'
                }
                try:
                    response = requests.get(url=url, headers=headers, timeout=3, verify=False,
                                            allow_redirects=False)  # 忽略ssl问题和禁止302、301跳转
                    response.encoding = 'utf-8'
                    threadLock.acquire()
                    re_handle(url, host, response.text, response.headers, response.status_code)  # url、host、响应体、响应头、响应码
                    threadLock.release()
                except Exception as e:
                    threadLock.acquire()
                    # print(e)
                    threadLock.release()
        threadLock.acquire()
        threadLock.release()


class handle_therad(threading.Thread):  # 独立线程 处理数据线程
    def __init__(self,path):
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        info_list = []  #
        while threads_complete:
            info_complete = True
            try:
                if len(info_list) == 0:
                    info = info_queue.get(timeout=3)
                    info_list.append(info)
                    with open(str(self.path) + '_host_boom_result.txt', 'a+', encoding='utf-8') as f:
                        f.write(str(info) + '\n')
                else:
                    info = info_queue.get(timeout=3)

                    for i in info_list:
                        if info[0] == i[0] and info[2] == i[2] and info[3] == i[3]:
                            info_complete = False
                            break
                    if info_complete:
                        info_list.append(info)
                        with open(str(self.path) + '_host_boom_result.txt', 'a+', encoding='utf-8') as f:
                            f.write(str(info) + '\n')
            except Exception as e:
                print(e)


class read_file_data(threading.Thread):  # 独立线程 加载数据，防止内存爆炸
    def __init__(self, num, ip_list, host_list):
        threading.Thread.__init__(self)
        self.num = num
        self.ip_list = ip_list
        self.host_list = host_list

    def run(self):  # 读取host.txt和ip.txt

        global queues_size
        queues_size = (len(self.ip_list) * len(self.host_list)) * 2
        for host in self.host_list:
            for ip in self.ip_list:
                queues.put((host, ip))
                global now_size
                now_size += 1
            while True:
                if queues.qsize() > self.num * 4:
                    global switch
                    switch = 0
                else:
                    break
        switch = 0


def re_handle(url, host, data, head, code):  # 网页返回内容处理
    try:
        title = re.search('<title>(.*)</title>', data).group(1)  # 获取标题
    except:
        title = u"获取标题失败"

    # 只要响应码200、301、302的，其他的都不要
    if code == 302 or code == 301:
        if 'Location' in head:
            info = (url, host, str(len(data)), str(code) + ':' + head['Location'])
            print(info, code)
            if '//cas.baidu.com' not in head['location'] and '//www.baidu.com' not in head['location'] and '//m.baidu.com' not in head['location']:
                info_queue.put(info)

    elif code == 200:
        info = (url, host, str(len(data)), title)
        print(info, code)
        if len(data) > 20:  # 去除掉一些无用数据
            info_queue.put(info)

    else:
        info = (url, host, str(len(data)), title)


def run_therad(num, ip_list, host_list,path):  # 创建新线程

    read_file_data_therads = read_file_data(num, ip_list, host_list)
    read_file_data_therads.start()

    while switch:
        continue

    threads = []
    for i in range(num):
        thread = get_therad(queues, i)
        thread.start()
        threads.append(thread)

    handle_therads = handle_therad(path)
    handle_therads.start()

    read_file_data_therads.join()
    for t in threads:
        t.join()
    global threads_complete
    threads_complete = False
    handle_therads.join()

def host(ip_list, host_list,path):
    print("=====开 始 匹 配=====")
    run_therad(20, ip_list, host_list,path)  # 线程数量
    print("已处理完成，匹配成功的保存在 :" + path)
