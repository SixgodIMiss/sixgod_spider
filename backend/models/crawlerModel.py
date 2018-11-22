# -*- coding: utf-8 -*-
from backend.model import Crawler, CrawlerConfig, Task
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 应用列表
def crawlerList(params):
    user_id = params['user_id']  # 用户ID
    page = params['page']
    items = Crawler.objects.get(user_id=user_id, valid=1)
    paginator = Paginator(items, 10)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result


# 应用详情
def crawlerConfig(crawler_id):
    try:
        item = Crawler.objects.get(id=crawler_id)
    except Exception as e:
        print(e)
        item = []
    return item


# 创建
def createCrawler(params):
    name = params['name']
    user_id = params['user_id']
    area = params['area']

    try:
        config = CrawlerConfig.objects.create(name=name, area=area, user_id=user_id)
        Crawler.objects.create(config_id=config.id)
    except Exception as e:
        print(e)
        return False
    return True
