# -*- coding: utf-8 -*-
import scrapy


class BasicSpider(scrapy.spiders.Spider):
    def close(self, reason):
        return reason

