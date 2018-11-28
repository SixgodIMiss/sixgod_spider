# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.model import Spider


def spiderList(params):
    page = params['page']
    size = params['size']
    name = params['name']

    # 查询
    pre = Spider.objects.order_by('province')
    if name:
        pre = pre.filter(name__contains=name)
    lists = pre.values('id', 'name', 'province', 'city', 'type', 'create_time', 'update_time')
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
        result['data'].append({
            'id': item['id'],
            'name': item['name'],
            'province': item['province'],
            'city': item['city'],
            'create_time': item['create_time'].strftime("%Y-%m-%d %H:%M:%S"),
            'update_time': item['update_time'].strftime("%Y-%m-%d %H:%M:%S")
        })
    return result


def save(params):
    result = True
    try:
        Spider.objects.create(name=params['name'], province=params['province'], city=params['city'])
    except Exception as e:
        result = False
    return result
