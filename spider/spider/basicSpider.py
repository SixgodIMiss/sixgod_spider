# -*- coding: utf-8 -*-
import os
import sys
import scrapy
import datetime

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'/mysql'))
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'/log'))
from mysqlModel import MysqlModel
from log import Log


class BasicSpider(scrapy.Spider):
    log = None
    model = None
    task_id = 0

    def __init__(self, task_id=0):
        if self.log is None:
            self.log = Log()

        if self.model is None:
            self.model = MysqlModel('master')

        self.task_id = task_id

    def insertProject(self, params):
        data = [
            params.get('project', ''), params.get('company', ''), params.get('date', ''), params.get('price', ''),
            params.get('architecter', ''), params.get('url', ''), self.task_id
        ]

        # 写日志
        logs = Log()
        logs.write('project', data)

        # 写数据库
        model = MysqlModel('master')
        model.insert("insert into project(`name`, `company`, `date`, `price`, `architecter`, `url`, `task_id`)"
                             "values (%s, %s, %s, %s, %s, %s, %s)", data)

        return True

    def close(self, reason):
        model = MysqlModel('master')
        model.update("update task set status = 'stop' WHERE id = %s", self.task_id)

        return reason


# model = MysqlModel('master')
# model.insert("insert into project(`name`, `company`, `date`, `price`, `architecter`)"
#                              " values (%s, %s, %s, %s, %s);", [1, 1, '2018-11-26', 1, 1])
