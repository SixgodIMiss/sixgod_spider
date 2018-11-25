# -*- coding: utf-8 -*-
import os
import sys
import scrapy

# 导入mysqlModel
sys.path.append(os.path.realpath(os.path.dirname(__file__)+'/mysql'))
from mysqlModel import MysqlModel


class BasicSpider(scrapy.Spider):

    def insertProject(self, params):
        data = [
            params.get('project', ''), params.get('company', ''), params.get('date', ''), params.get('price', ''),
            params.get('architecter', '')
        ]
        model = MysqlModel('master')
        result = model.insertOne("insert into project(`name`, `company`, `date`, `price`, `architecter`)"
                             "values (%s, %s, %s, %s, %s)", data)
        print(result)

    def close(self, reason):
        return reason

