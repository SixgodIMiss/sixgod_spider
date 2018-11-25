# -*- coding: utf-8 -*-
import os
import sys
import scrapy
from scrapy.http import Request
import json

# 导入basic
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from basicSpider import BasicSpider


class ProjectSpider(BasicSpider):
    name = 'Hangzhou'
    allowed_domains = ['hzctc.cn']
    start_urls = [
        'http://www.hzctc.cn/SecondPage/GetNotice'
    ]

    def start_requests(self):
        formData = {
            'area': '72',
            'afficheType': '22',
            'IsToday': '',
            'title': '',
            'proID': '',
            'number': '',
            '_search': 'false',
            'nd': '1543066751752',
            'rows': '10',
            'page': '1',
            'sidx': 'PublishStartTime',
            'sord': 'desc'
        }
        return [scrapy.FormRequest('http://www.hzctc.cn/SecondPage/GetNotice',
                                   method='POST',
                                   formdata=formData,
                                   callback=self.get_page)]

    # 获取每页的所有链接
    def get_page(self, response):
        result = json.loads(response.body.decode('utf8'))
        page_count = result['total']
        formData = {
            'area': '72',
            'afficheType': '28',
            'IsToday': '',
            'title': '',
            'proID': '',
            'number': '',
            '_search': 'false',
            'nd': '1543066751752',
            'rows': '10',
            'page': '1',
            'sidx': 'PublishStartTime',
            'sord': 'desc'
        }

        for i in range(page_count):
            formData['page'] = str(i+1)
            # print(i+1)
            yield scrapy.FormRequest('http://www.hzctc.cn/SecondPage/GetNotice',
                                     method='POST',
                                     formdata=formData,
                                     callback=self.get_list)

    # 获取当前页的链接
    def get_list(self, response):
        # print(response)
        result = json.loads(response.body.decode('utf8'))
        rows = result['rows']
        base_link = 'http://www.hzctc.cn/AfficheShow/Home?AfficheID='

        for row in rows:
            rid = row['ID']
            link = base_link + rid + '&IsInner=0&ModuleID=28'
            yield Request(url=link, callback=self.get_info, encoding='utf-8')

    def get_info(self, response):
        get_project = response.xpath('/html/body/div[3]/div[2]/div[1]/text()[1]').extract()
        get_date = response.xpath('/html/body/div[3]/div[2]/div[1]/text()[2]').extract()
        get_company = response.xpath('//*[@id="lb_zbddw"]/text()').extract()
        get_architecter = response.xpath('//*[@id="lb_xmjl"]/text()').extract()
        get_price = response.xpath('//*[@id="lb_zbjg"]/text()').extract()

        # 中标公司
        company = get_company[0].replace('\r\n', '').replace(' ', '')
        # 中标项目
        project = get_project[0].replace('\r\n', '').replace(' ', '')
        # 中标日期
        date = get_date[0].replace('\r\n', '').replace(' ', '')
        # 中标金额
        price = get_price[0].replace('\r\n', '').replace(' ', '')
        price = price.replace('万元', '') if '万元' in price else int(price.replace('元'))/10000
        # 建造师
        architecter = get_architecter[0].replace('\r\n', '').replace(' ', '')

        result = {
            'company': company,
            'project': project,
            'date': date,
            'price': price,
            'architecter': architecter
        }
        self.insertProject(result)

