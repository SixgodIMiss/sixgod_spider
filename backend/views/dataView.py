# -*- coding: utf-8 -*-
import django  # 多进程用
django.setup()
from django.http import JsonResponse
from backend.views import userView
from backend.models import dataModel, crawlerModel
import datetime, time, json
import multiprocessing, urllib, urllib2


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

    crawler_id = post.get('crawler_id', 0)
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


# 数据迁移
def transfer(request):
    userView.checkLogin(request)
    post = request.POST

    if post.get('type', None) == "1":
        params = {
            'api': post.get('api', ''),
            'format': post.get('format', ''),
            'per': post.get('per', 10)
        }
        # 防止自己调用自己
        if '/data/transfer' in params['api']:
            return JsonResponse(params)
    else:
        params = {
            'host': post.get('host', ''),
            'type': post.get('type', "1"),
            'port': post.get('post', 3306),
            'user': post.get('user', ''),
            'password': post.get('password', ''),
            'db_name': post.get('db_name', ''),
            'db_table': post.get('db_table', '')
        }

    start = multiprocessing.Process(
        target=transferProcess, kwargs=params
    )
    start.daemon = True
    start.start()

    return JsonResponse(params)


def transferProcess(**kwargs):
    type = kwargs.get('type')

    data = {
        'crawler_id': 1,
        'cPage': 1,
        'pSize': 1
    }
    data = urllib.urlencode(data)
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/x-www-form-urlencoded"}
    try:
        req = urllib2.Request(url='http://www.google.com', data=data, headers=header_dict)
        res = urllib2.urlopen(req, timeout=8)
        response = res.read()
    except Exception as e:
        print(e.args[0])
    return True

