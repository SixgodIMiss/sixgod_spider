# -*- coding: utf-8 -*-
import datetime
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.model import Project
from django.db import connection


def timeline(params):
    data = {}
    try:
        # items = Project.objects.filter(task_id=params['task_id'], create_time__range=(
        #     params['timestamps'][0], params['timestamps'][params['number'] - 1]
        # )).values('id', 'create_time')
        items = Project.objects.filter(task_id=params['task_id'], create_time__gte=params['timestamps'][0]).values('id','create_time')

        # sql = 'select id, create_time from project where task_id=' + str(params['task_id']) + ' and create_time>="' + \
        #       params['timestamps'][0] + '" and create_time<="' + params['timestamps'][params['number'] - 1] + '"'
        # items = Project.objects.raw(sql)
        # print(params['timestamps'])

        # 统计每个时间点抓取条数
        for item in items:
            item['create_time'] = item['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            print(item)

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
    task_id = params['task_id']  # 哪个爬虫应用的
    # start = params['start']  # 起始时间
    # end = params['end'] if params['end'] else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result = {
        'data': [],
        'status': 'success',
        'totals': ''
    }

    try:
        lists = Project.objects.order_by('-create_time').filter(task_id=task_id).values(
            'id', 'name', 'company', 'date', 'price', 'architecter', 'url', 'create_time'
        )

        # 分页
        paginator = Paginator(lists, size)
        items = paginator.page(page)
        result['totals'] = paginator.count

        for item in items:
            result['data'].append({
                'id': str(item['id']),
                'name': item['name'],
                'company': item['company'],
                'project_date': item['date'].strftime("%Y-%m-%d"),
                'price': item['price'],
                'architecter': item['architecter'],
                'url': item['url'],
                'create_time': item['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            })
    except Exception as e:
        print(e)

    return result


# 检测任务是否爬到数据并返回条数
def checkTaskData(task_id):
    number = 0
    try:
        number = Project.objects.filter(task_id=task_id).count()
    except Exception as e:
        print(e)

    return number
