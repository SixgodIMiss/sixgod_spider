# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 中标公告
class ProjectItem(scrapy.Item):
    company = scrapy.Field()
    project = scrapy.Field()  # 项目
    architecter = scrapy.Field()  # 建造师
    date = scrapy.Field()  # 中标日期
    price = scrapy.Field()  # 中标金额

