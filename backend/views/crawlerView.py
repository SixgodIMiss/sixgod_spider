# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'sixgod_spider.settings'
import django  # 多进程用
django.setup()
import sys
import multiprocessing
import subprocess
import json
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from backend.views import userView
from backend.models import crawlerModel
from django.db import connection


# 首页
def index(request):
    logined = request.session.get('user_id', None)
    if logined is None:
        return HttpResponseRedirect('/login')
    return render(request, 'crawler/list.html')


# 用户爬虫应用列表
def crawlerList(request):
    user_id = userView.checkLogin(request)
    post = request.POST
    params = {
        'user_id': user_id,
        'page': int(post.get('cPage', 1)),
        'size': int(post.get('pSize', 20)),
        'name': str(post.get('crawler_name', None)),
        'status': post.get('status', 0)
    }
    result = crawlerModel.crawlerList(params)
    return JsonResponse(result)


# 应用配置页
def crawlerConfig(request):
    user_id = userView.checkLogin(request)
    crawler_id = request.GET.get('id', None)
    result = {
        'active': 'create'
    }
    if crawler_id is not None:
        result = crawlerModel.crawlerConfig(crawler_id=crawler_id, user_id=user_id)
        result['active'] = 'update'
    return render(request, 'crawler/config.html', result)


# 应用详情页
def crawlerInfo(request):
    user_id = userView.checkLogin(request)
    crawler_id = request.GET.get('id', None)
    result = {}
    if crawler_id is not None:
        result = crawlerModel.crawlerConfig(crawler_id=crawler_id, user_id=user_id)

    return render(request, 'crawler/info.html', result)


# 保存配置
def crawlerSave(request):
    user_id = userView.checkLogin(request)
    post = request.POST
    params = {
        'user_id': user_id,
        'name': post.get('name', ''),
        'province': post.get('province', ''),
        'city': post.get('city', ''),
        'crawler_id': post.get('id', '')
    }

    # 不传ID就凉
    if params['crawler_id'] == '' or params['province'] == '' or params['city'] == '':
        result = 'error'
    else:
        result = crawlerModel.saveCrawler(params)
    return JsonResponse({'status': result})


def startProcess(crawler_id, spiders):
    file = os.path.dirname(os.path.abspath(__file__)) + '/log.txt'
    f = open(file, 'a+')
    f.write(spiders+'\n')
    f.close()
    return True

def handler(request):
    post = request.POST
    user_id = userView.checkLogin(request)
    result = {
        'status': 'fail',
        'reason': 'Error'
    }

    crawler_id = post.get('id', None)
    active = post.get('active', None)
    actives = ['start', 'stop', 'pause', 'restart', 'del']
    # 参数验证
    if crawler_id is None or crawler_id == '' or active not in actives:
        result['reason'] = '参数有问题'
        return JsonResponse(result)

    check = crawlerModel.checkUserCrawler(crawler_id=crawler_id, user_id=user_id)
    # 判断用户是否有权操作该应用
    if check is False:
        result['reason'] = '无权操作'
        return JsonResponse(result)
    # 判断爬虫运行状况
    condition = {
        'starting': '爬虫正在启动中',
        'running': '爬虫正在运行',
        'stopping': '爬虫正在停止',
        'stop': '爬虫已停止'
    }
    status = check.task.status
    if active == 'start' and status != 'stop':
        result['reason'] = condition.get(status)
    elif active == 'stop' and status != 'running':
        result['reason'] = condition.get(status)
    elif active == 'del' and status != 'stop':
        result['reason'] = condition.get(status)
    if result['reason'] != 'Error':
        return JsonResponse(result)

    process_name = check.config.name
    spiders = check.config.spiders
    print(spiders)

    # start = multiprocessing.Process(
    #     name=process_name, target=startProcess, args=(crawler_id, 'zhejiang')
    # )
    # start.daemon = True
    # start.start()
    # print(start.pid)
    # start.join()

    # scrapy_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/spider')
    # subprocess.check_call('scrapy crawl Zhejiang_Hangzhou --no-log', cwd=scrapy_path)

    return JsonResponse(result)



