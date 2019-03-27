# -*- coding: utf-8 -*-
import datetime
from backend.model import Crawler, CrawlerConfig, Task, Spider
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


# ***************
# 应用列表
def crawlerList(params):
    user_id = params['user_id']  # 用户ID
    page = params['page']
    size = params['size']
    name = params['name']
    status = params['status'] if params['status'] != 0 else None
    result = {
        'data': [],
        'status': 'success',
        'totals': ''
    }

    # 查询
    pre = Crawler.objects.order_by('-id').filter(config__user=user_id, valid=1)
    if name:
        # 带名称模糊查询
        pre = pre.filter(config__name__contains=name)
    if status != '0':
        # 状态查询
        pre = pre.filter(task__status=status)
    lists = pre.values(
        'id', 'valid',
        'config_id', 'config__name', 'config__province', 'config__city', 'config__create_time', 'config__user__name',
        'task_id', 'task__status', 'task__start', 'task__end'
    )
    # print(lists)

    # 分页
    paginator = Paginator(lists, size)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    result['totals'] = paginator.count

    # 格式化
    for item in items:
        # print(item)
        result['data'].append({
            'id': item['id'],
            'config_id': item['config_id'],
            'name': item['config__name'],
            'user': item['config__user__name'],
            'province': item['config__province'],
            'city': item['config__city'],
            'task_id': item['task_id'],
            'status': item['task__status'],
            'start': item['task__start'],
            'end': item['task__end'],
            'create_time': item['config__create_time'].strftime("%Y-%m-%d %H:%M:%S")
        })
    return result


# 应用详情
def crawlerConfig(crawler_id, user_id):
    result = {}
    try:
        item = Crawler.objects.get(id=crawler_id, config__user_id__exact=user_id)
        if item:
            # 将对应的爬虫程序名查出来
            spiders = item.config.spiders
            spider_names = []
            if spiders:
                spider_names = getSpiders(spiders)

            result = {
                'id': item.id,
                'name': item.config.name,
                'user': item.config.user.name,
                'province': item.config.province,
                'city': item.config.city,
                'spiders': spider_names,
                'create_time': item.config.create_time,
                'update_time': item.config.update_time,
            }
    except Exception as e:
        print(e)
    return result


# 创建
def saveCrawler(params):
    name = params['name']
    user_id = params['user_id']
    province = params['province']
    city = params['city']
    crawler_id = params['crawler_id']

    try:
        # 一定要配置有省市，才能将应用和程序对应起来
        spider_arr = []
        if province == '' or city == '':
            return False
        else:
            spiders = Spider.objects.filter(province=province, city=city).values('id')

            for spider_id in spiders:
                spider_arr.append(str(spider_id['id']))
        spider_str = '_'.join(spider_arr)  # 以下划线作分割
        if spider_str == '':
            return False

        if crawler_id == '':
            # 创建
            config = CrawlerConfig.objects.create(name=name, province=province, city=city,
                                                  user_id=user_id, spiders=spider_str)
            task = Task.objects.create(status='stop', crawler_id=0)
            crawler = Crawler.objects.create(config_id=config.id, task_id=task.id)
            task.crawler_id = crawler.id
            task.save()
        else:
            # 修改
            config_id = Crawler.objects.get(id=crawler_id).config_id
            CrawlerConfig.objects.filter(id=config_id).update(name=name, province=province, city=city,
                                                              spiders=spider_str)
    except Exception as e:
        print(e)
        return False
    return True


# 获取对应的爬虫程序
def getSpiders(spider_ids):
    spider_arr = spider_ids.split('_')
    spider_names = []
    for spider_id in spider_arr:
        name = Spider.objects.get(id=spider_id).name
        spider_names.append(name)
    return spider_names


# 检测爬虫以及返回爬虫运行状态
def checkUserCrawler(crawler_id, user_id):
    check = False
    try:
        check = Crawler.objects.get(id=crawler_id, config__user_id=user_id, valid=1)
    except Exception as e:
        print(e)
    return check


# 删除爬虫
def crawlerDel(crawler_id):
    result = False
    try:
        result = Crawler.objects.filter(id=crawler_id).update(valid=0)
    except Exception as e:
        print(e)
    return result


# 修改任务状态 pid->爬虫程序运行所在的子进程ID
def taskHandler(crawler_id, active, pid=0):
    finish_status = ''  # 修改过后的状态
    result = {
        'task': 0,
        'status': '',
    }
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        crawler = Crawler.objects.get(id=crawler_id)
        status = crawler.task.status  # 任务当前状态

        # 状态的改变是根据上一个状态而进行改变
        if active == 'start':
            # 启动相当于创建一个任务
            finish_status = 'starting'
            new_task = Task.objects.create(crawler_id=crawler_id, status=finish_status, start=now, pid=pid)
            # 将新任务绑到应用上
            crawler.task_id = new_task.id
            crawler.save()

            result['status'] = finish_status
            result['task'] = crawler.task_id
            return result
        elif active == 'stop':
            # 先不考虑stopping状态
            finish_status = 'stop'
        elif active == 'finish':
            if status == 'starting':
                finish_status = 'running'
            elif status == 'running':
                finish_status = 'stopping'
            elif status == 'stopping':
                finish_status = 'stop'
            else:
                finish_status = status

        # 所有任务状态的改变都要严谨点
        if finish_status != status:
            if finish_status == 'starting':
                crawler.task.start = now
            elif finish_status == 'stopping':
                crawler.task.end = now

        # 修改完应用对应的任务后保存
        crawler.task.status = finish_status
        crawler.task.save()

        result['task'] = crawler.task.id
        result['status'] = finish_status
    except Exception as e:
        return False
    return result


# 爬虫任务详情
def taskInfo(crawler_id):
    result = {}
    try:
        crawler = Crawler.objects.get(id=crawler_id)

        if crawler:
            result = {
                'id': crawler.id,
                'task_id': crawler.task_id,
                'name': crawler.config.name,
                'status': crawler.task.status,
                'user_id': crawler.config.user_id,
                'start': crawler.task.start.strftime("%Y-%m-%d %H:%M:%S")if crawler.task.start else '',
                'end': crawler.task.end.strftime("%Y-%m-%d %H:%M:%S") if crawler.task.end else ''
            }
    except Exception as e:
        print(e)
    return result


