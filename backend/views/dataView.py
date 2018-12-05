# -*- coding: utf-8 -*-
from django.http import JsonResponse
from backend.views import userView
from backend.models import dataModel, crawlerModel
import datetime, time


def timeline(request):
    user_id = userView.checkLogin(request)
    post = request.POST
    result = {
        'reason': '',
        'status': 'fail',
        'data': {}
    }

    crawler_id = post.get('crawler_id', None)  # 爬虫应用ID
    deadline = post.get('deadline', datetime.datetime.now())  # 最新时间节点
    number = int(post.get('number', 10))  # 时间间隔默认1s

    # 验参
    if crawler_id is None or crawler_id == '':
        result['reason'] = '参数不正确'
        return JsonResponse(result)

    # 看爬虫是不是自己的
    check_crawler = crawlerModel.checkUserCrawler(crawler_id, user_id)
    if check_crawler is False:
        result['reason'] = '非法操作'
        return JsonResponse(result)

    # 时间轴的时间节点
    timestamps = []
    now = datetime.datetime.now()
    for i in range(0, number):
        times = now - datetime.timedelta(hours=0, minutes=0, seconds=(1*i))
        timestamps.append(times.strftime("%Y-%m-%d %H:%M:%S"))
    timestamps.sort()
    # print(123)

    params = {
        'task_id': check_crawler.task_id,
        'timestamps': timestamps,
        'number': number
    }
    query = dataModel.timeline(params)
    # print(query)
    if query:
        result['status'] = 'success'
    result['data'] = query

    return JsonResponse(result)


# 爬虫应用对应的数据
def dataList(request):
    user_id = userView.checkLogin(request)
    post = request.POST
    crawler_id = post.get('crawler_id', None)
    result = {
        'data': [],
        'status': 'success',
        'totals': ''
    }

    # 验参
    check = crawlerModel.checkUserCrawler(crawler_id, user_id)
    if crawler_id is None or crawler_id == '' or check is False:
        return JsonResponse(result)

    # 查看任务运行状态
    task = crawlerModel.taskInfo(crawler_id)

    params = {
        'task_id': task['task_id'],
        'page': post.get('cPage', 1),
        'size': post.get('pSize', 10),
        # 'start': task['start'],
        # 'end': task['end'],
    }
    # print(params)
    result = dataModel.query(params)
    return JsonResponse(result)

