# -*- coding: utf-8 -*-
import datetime
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.model import Project


def timeline(params):
    data = {}
    try:
        items = Project.objects.filter(crawler_id=params['crawler_id'], create_time__gte=params['timestamps'][0],
                                     create_time__lte=params['timestamps'][params['number']-1]).values('id', 'create_time')
        # print(items)

        # 统计每个时间点抓取条数
        for item in items:
            item['create_time'] = item['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            if item['create_time'] in params['timestamps']:
                if data.get(item['create_time'], None) is None:
                    data[item['create_time']] = 1
                else:
                    data[item['create_time']] += 1

    except Exception as e:
        print(e)

    return data


# 数据查询
def query(params):
    page = params['page']
    size = params['size']
    crawler_id = params['crawler_id']  # 哪个爬虫应用的
    start = params['start']  # 起始时间
    end = params['end'] if params['end'] else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print(end)

    result = {
        'data': [],
        'status': 'success',
        'totals': ''
    }

    try:
        lists = Project.objects.filter(crawler_id=crawler_id, create_time__gte=start, create_time__lte=end).values(
            'id', 'name', 'company', 'date', 'price', 'architecter', 'url', 'create_time'
        )

        # 分页
        paginator = Paginator(lists, size)
        items = paginator.page(page)
        result['totals'] = paginator.num_pages

        for item in items:
            print(item)
            result['data'].append({
                'id': str(item['id']),
                'name': item['name'],
                'company': item['company'],
                'date': item['date'].strftime("%Y-%m-%d"),
                'price': item['price'],
                'architecter': item['architecter'],
                'url': item['url'],
                'create_time': item['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            })
    except Exception as e:
        print(e)

    return result
