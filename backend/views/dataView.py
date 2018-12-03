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
    deadline = post.get('deadline', datetime.datetime.now().strftime("%H:%M:%S"))  # 最新时间节点
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
    # today = datetime.datetime.now().strftime('%Y-%m-%d')
    today = '2018-11-27'
    timestamps = []
    for i in range(0, number):
        timestamps.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.mktime(time.strptime(
            today+' '+deadline, "%Y-%m-%d %H:%M:%S"))) - i)))
    timestamps.sort()

    params = {
        'crawler_id': crawler_id,
        'timestamps': timestamps,
        'number': number
    }
    query = dataModel.timeline(params)
    if query:
        result['status'] = 'success'
    result['data'] = query

    return JsonResponse(result)


def dataList(request):
    user_id = userView.checkLogin(request)
    post = request.POST
    result = {
        'data': [],
        'status': 'fail',
        'totals': 0
    }
    return JsonResponse(result)

