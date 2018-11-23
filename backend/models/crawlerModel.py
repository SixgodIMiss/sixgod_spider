# -*- coding: utf-8 -*-
from backend.model import Crawler, CrawlerConfig, Task
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


# ***************
# 应用列表
def crawlerList(params):
    user_id = params['user_id']  # 用户ID
    page = params['page']

    # 查询
    lists = Crawler.objects.order_by('-id').filter(config__user=user_id, valid=1).values(
        'id', 'config_id', 'config__name', 'config__area', 'valid', 'config__create_time', 'config__user__name')
    # 分页
    paginator = Paginator(lists, 10)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    result = {
        'status': 'success',
        'data': [],
        'totals': items.number
    }
    # 格式化
    for item in items:
        # print(item)
        result['data'].append({
            'id': item['id'],
            'config_id': item['config_id'],
            'name': item['config__name'],
            'user': item['config__user__name'],
            'area': item['config__area'],
            'create_time': item['config__create_time']
        })
    return result


# 应用详情
def crawlerConfig(crawler_id, user_id):
    result = {}
    try:
        item = Crawler.objects.get(id=crawler_id, config__user_id__exact=user_id)
        if item is not None:
            result = {
                'name': item.config.name,
                'user': item.config.user.name,
                'area': item.config.area,
                'create_time': item.create_time
            }
    except Exception as e:
        print(e)
    return result


# 创建
def saveCrawler(params):
    name = params['name']
    user_id = params.user_id
    area = params['area']
    crawler_id = params.get('crawler_id', None)

    try:
        if crawler_id is None or crawler_id == "":
            config = CrawlerConfig.objects.create(name=name, area=area, user_id=user_id)
            Crawler.objects.create(config_id=config.id)
        else:
            config_id = Crawler.objects.get(id=crawler_id).config_id
            CrawlerConfig.objects.filter(id=config_id).update(name=name, area=area)
    except Exception as e:
        return False
    return True
