# -*- coding: utf-8 -*-
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.model import Spider, SlfSpider, SlfMonitor
from django.db.models import Count, QuerySet


def spiderList(params):
    page = params['page']
    size = params['size']
    name = params['name']
    status = params['status']
    # print(status == 0)

    # 查询
    pre = SlfSpider.objects.using('slf').order_by('status')
    if name:
        pre = pre.filter(program_name__contains=name)
    if status:
        pre = pre.filter(status__contains=status)
    lists = pre.values()

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
        'totals': paginator.count
    }
    # 格式化
    for item in items:
        result['data'].append({
            'id': item['id'],
            'name': item['program_name'],
            'source': item['source'],
            'status': item['status'],
            'url_name': item['url_name'],
            'province': item['ch_area'],
            'city': item['ch_city'],
            'county': item['ch_region'],
            'type': item['type'],
            'who': item['who'],
            'update_who': item['update_who'],
            'check_time': item['check_time'].strftime("%Y-%m-%d") if item['check_time'] else ''
        })
    return result


def save(params):
    result = True
    try:
        Spider.objects.create(name=params['name'], province=params['province'], city=params['city'])
    except Exception as e:
        result = False
    return result


# 所有执行节点
def monitor(params):
    page = params['page']
    size = params['size']
    name = params['name']
    status = params['status']
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    # 查询条件
    pre = SlfMonitor.objects.using('slf').order_by('-create_time').filter(create_time__contains=today)
    if name and name != "":
        pre = pre.filter(spider__program_name__contains=name)
    if status in ["1", "2", "3", "4"]:
        pre = pre.filter(status__contains=status)

    lists = pre.values('id', 'spider_id', 'spider__program_name', 'spider__source', 'spider__url_name', 'status', 'reason', 'create_time')
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
        'totals': paginator.count
    }
    for item in items:
        result['data'].append({
            'id': item['id'],
            'spider_id': item['spider_id'],
            'name': item['spider__program_name'],
            'url': item['spider__url_name'],
            'source': item['spider__source'],
            'status': item['status'],
            'reason': item['reason'],
            # 'hash': item['hash'],
            'create_time': item['create_time'].strftime("%Y-%m-%d %H:%M:%S")
        })

    return result


# 最后状态
def monitorUnique(params):
    page = params['page']
    size = params['size']
    name = params['name']
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    # 查询条件
    pre = SlfMonitor.objects.using('slf').filter(create_time__contains=today)
    if name and name != "":
        pre = pre.filter(spider__program_name__contains=name)

    lists = pre.values('hash', 'spider_id').annotate(Count('hash'))
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
        'totals': paginator.count
    }

    model = SlfMonitor.objects.using('slf').order_by('-create_time')
    for item in items:
        record = model.filter(hash=item['hash'], spider_id=item['spider_id']).values('id', 'spider__program_name', 'spider__url_name', 'spider__source', 'status', 'reason', 'create_time')
        result['data'].append({
            'id': record[0]['id'],
            'spider_id': item['spider_id'],
            'name': record[0]['spider__program_name'],
            'source': record[0]['spider__source'],
            'url': record[0]['spider__url_name'],
            'status': record[0]['status'],
            'reason': record[0]['reason'],
            'create_time': record[0]['create_time'].strftime("%Y-%m-%d %H:%M:%S")
        })
    return result
