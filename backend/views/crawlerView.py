# -*- coding: utf-8 -*-

import os, signal
import sys
# sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/spider'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'sixgod_spider.settings'
# os.environ['SCRAPY_SETTINGS_MODULE'] = 'spiders.settings'

import django  # 多进程用
django.setup()
import multiprocessing, subprocess
import datetime, time
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from backend.views import userView
from backend.models import crawlerModel, dataModel
from twisted.internet import reactor


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
    result = {
        'status': 'fail',
        'msg': ''
    }

    # 不传ID就凉
    if params['province'] == '' or params['city'] == '':
        result['msg'] = '缺少省市'
    else:
        if crawlerModel.saveCrawler(params):
            result['status'] = 'success'
        else:
            result['msg'] = '保存失败'
    return JsonResponse(result)


def handler(request):
    post = request.POST
    user_id = userView.checkLogin(request)
    result = {
        'status': 'fail',
        'reason': ''
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
    status = check.task.status  # 当前状态
    if active == 'start':
        if status != 'stop':
            result['reason'] = condition.get(status)
        else:
            # 启动
            spiders = check.config.spiders
            if spiders == '':
                result['reason'] = '没有对应的爬虫程序'
            else:
                task = crawlerModel.taskHandler(crawler_id, 'start')
                if task:
                    result['status'] = 'success'
                else:
                    result['reason'] = '启动失败'

                # 子进程启动爬虫
                spider_names = crawlerModel.getSpiders(spiders)
                startProcess(task['task'], spider_names)

    elif active == 'stop':
        stopProcess(check.task)
        if crawlerModel.taskHandler(crawler_id, 'stop'):
            result['status'] = 'success'
        else:
            result['reason'] = '停止失败'
    elif active == 'del':
        if status != 'stop':
            result['reason'] = condition.get(status)
        else:
            if crawlerModel.crawlerDel(crawler_id):
                result['status'] = 'success'
            else:
                result['reason'] = '删除失败'

    # process_name = check.config.name
    # spiders = check.config.spiders
    # print(spiders)

    # scrapy_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/spider')
    # subprocess.check_call('scrapy crawl Zhejiang_Hangzhou --no-log', cwd=scrapy_path)

    return JsonResponse(result)


# 执行子进程并返回pid
def startProcess(task_id, spiders):
    # 启动
    # process_name = 'spider-' + str(task_id) + '-' + str(datetime.datetime.now().strftime("%m_%d_%H_%M"))
    # start = multiprocessing.Process(
    #     name=process_name, target=multiSpider, args=(task_id, spiders)
    # )
    # start.daemon = True
    # start.start()
    # # start.join()
    # pid = start.pid

    # 另外启动方式
    scrapy_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/spider')
    pid = subprocess.Popen('scrapy crawl '+spiders[0]+' -a task_id='+str(task_id), cwd=scrapy_path, shell=True).pid

    # 将pid绑定task
    task = crawlerModel.Task.objects.get(id=task_id)
    task.pid = pid
    task.save()

    return True


def multiSpider(task_id, spiders):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spiders[0], task_id=task_id)
    process.start()


# 关闭爬虫进程
def stopProcess(task):
    # p = psutil.Process(pid=int(pid))
    try:
        os.kill(task.pid, signal.SIGILL)
    except Exception as e:
        print(e)
    finally:
        task.status = 'stop'
        task.end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task.save()
        return True


# 应用爬取详情
def taskInfo(request):
    user_id = userView.checkLogin(request)
    crawler_id = request.GET.get('id', None)

    if crawler_id is None or crawler_id == '' or crawlerModel.checkUserCrawler(crawler_id, user_id) is False:
        return HttpResponseRedirect('/index')

    result = crawlerModel.taskInfo(crawler_id)
    return render(request, 'crawler/view.html', result)


# 监测爬虫运行状态
def checkStatus(request):
    use_id = userView.checkLogin(request)
    crawler_id = request.POST.get('id', None)
    result = {
        'msg': '',
        'status': '',
        'number': 0
    }

    if crawler_id is None or crawler_id == '':
        result['msg'] = '参数'
        return JsonResponse(result)

    crawler = crawlerModel.checkUserCrawler(crawler_id, use_id)
    if crawler:
        result['status'] = crawler.task.status
    else:
        result['msg'] = '非法操作'

    # 如果爬到了数据就变成running
    task = crawler.task
    result['number'] = dataModel.checkTaskData(task.id)
    if task.status == 'starting' and result['number'] != '':
        task.status = 'running'
        task.save()
        result['status'] = 'running'

    return JsonResponse(result)

