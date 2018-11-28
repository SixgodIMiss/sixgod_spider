# -*- coding: utf-8 -*-
import time
from backend.model import Crawler, CrawlerConfig, Task, Spider
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


# ***************
# 应用列表
def crawlerList(params):
    user_id = params['user_id']  # 用户ID
    page = params['page']
    size = params['size']
    name = params['name']
    status = params['status'] if params['status'] != 0 else None

    # 查询
    pre = Crawler.objects.order_by('-id').filter(config__user=user_id, valid=1)
    if name:
        # 带名称模糊查询
        pre = pre.filter(config__name__contains=name)
    if status != '0':
        # 状态查询
        pre = pre.filter(task__status=status)
    lists = pre.values(
        'id', 'valid',
        'config_id', 'config__name', 'config__province', 'config__city', 'config__create_time', 'config__user__name',
        'task_id', 'task__status', 'task__start', 'task__end'
    )
    # 分页
    paginator = Paginator(lists, size)
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
            'province': item['config__province'],
            'city': item['config__city'],
            'task_id': item['task_id'],
            'status': item['task__status'],
            'start': item['task__start'],
            'end': item['task__end'],
            'create_time': item['config__create_time'].strftime("%Y-%m-%d %H:%M:%S")
        })
    return result


# 应用详情
def crawlerConfig(crawler_id, user_id):
    result = {}
    try:
        item = Crawler.objects.get(id=crawler_id, config__user_id__exact=user_id)
        if item:
            # 将对应的爬虫程序名查出来
            spiders = item.config.spiders
            spider_names = []
            if spiders:
                spider_arr = spiders.split('_')
                for spider_id in spider_arr:
                    name = Spider.objects.get(id=spider_id).name
                    spider_names.append(name)

            result = {
                'id': item.id,
                'name': item.config.name,
                'user': item.config.user.name,
                'province': item.config.province,
                'city': item.config.city,
                'spiders': spider_names,
                'create_time': item.config.create_time,
                'update_time': item.config.update_time,
            }
    except Exception as e:
        print(e)
    return result


# 创建
def saveCrawler(params):
    name = params['name']
    user_id = params['user_id']
    province = params['province']
    city = params['city']
    crawler_id = params['crawler_id']
    try:
        # 一定要配置有省市，才能将应用和程序对应起来
        spider_arr = []
        if province == '' or city == '':
            return False
        else:
            spiders = Spider.objects.filter(province=province, city=city).values('id')
            for spider_id in spiders:
                spider_arr.append(str(spider_id['id']))
        spider_str = '_'.join(spider_arr)

        if crawler_id == '':
            # 创建
            config = CrawlerConfig.objects.create(name=name, province=province, city=city, user_id=user_id, spiders=spider_str)
            task = Task.objects.create(status='stop')
            Crawler.objects.create(config_id=config.id, task_id=task.id)
        else:
            # 修改
            config_id = Crawler.objects.get(id=crawler_id).config_id
            CrawlerConfig.objects.filter(id=config_id).update(name=name, province=province, city=city, spiders=spider_str)
    except Exception as e:
        return False
    return True


# 检测爬虫以及返回爬虫运行状态
def checkUserCrawler(crawler_id, user_id):
    try:
        check = Crawler.objects.get(id=crawler_id, config__user_id=user_id)
    except Exception as e:
        check = False
    return check
