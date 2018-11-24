# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json


class ProjectSpider(scrapy.spiders.Spider):
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
            yield Request(url=link, callback=self.get_info)

    def get_info(self, response):
        project = response.xpath('/html/body/div[3]/div[2]/div[1]/text()[1]').extract().str_replace('\r\n', '').str_replace(' ', '')
        date = response.xpath('/html/body/div[3]/div[2]/div[1]/text()[2]').extract().str_replace('\r\n', '').str_replace(' ', '')
        company = response.xpath('//*[@id="lb_zbddw"]').extract()
        architecter = response.xpath('//*[@id="lb_xmjl"]').extract()
        price = response.xpath('//*[@id="lb_zbjg"]').extract()



