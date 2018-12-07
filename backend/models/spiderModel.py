# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.model import Spider, SlfSpider


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
