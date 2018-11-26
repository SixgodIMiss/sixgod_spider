# -*- coding: utf-8 -*-
import os
import datetime
import json


class Log(object):
    base_path = ''
    log_path = ''
    project = {
        'name': '',
        'company': '',
        'date': '',
        'price': '',
        'architecter': '',
        'time': '',
    }  # project的数据格式
    error = {
        'spider': '',
        'url': '',
        'data': '',
        'reason': '',
        'time': ''
    }  # error日志格式

    def __init__(self):
        # today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        month = datetime.datetime.now().strftime("%Y-%m")
        day = datetime.datetime.now().strftime("%d")

        # 初始化目录
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        if os.path.exists(self.base_path + '/record/' + month) is False:
            os.mkdir(self.base_path + '/record/' + month)
        if os.path.exists(self.base_path + '/record/' + month + '/' + day) is False:
            os.mkdir(self.base_path + '/record/' + month + '/' + day)
        self.log_path = self.base_path + '/record/' + month + '/' + day

    def write(self, type='project', data={}):
        file = self.log_path
        record = None

        if type == 'project':
            # 工程爬取数据写入日志
            file = os.path.abspath(file + '/project.log')
            self.project['name'] = data[0]
            self.project['company'] = data[1]
            self.project['date'] = data[2]
            self.project['price'] = str(data[3])
            self.project['architecter'] = data[4]
            self.project['time'] = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            record = self.project
        elif type == 'error':
            # 错误写入日志
            file = os.path.abspath(file + '/error.log')
            self.error = data
            record = self.error

        f = open(file, 'a+')
        f.write(json.dumps(record)+'\n')
        f.close()

        return file


# log = Log()
# log.write('project', {
#     'time': datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
#     'company': '',
#     'name': '',
#     'date': '',
#     'price': '',
#     'architecer': ''
# })
