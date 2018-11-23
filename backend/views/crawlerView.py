# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from backend.views import userView
from backend.models import crawlerModel


# 首页
def index(request):
    logined = request.session.get('user_id', None)
    if logined is None:
        return HttpResponseRedirect('/login')
    return render(request, 'crawler/list.html')


# 用户爬虫应用列表
def crawlerList(request):
    user_id = userView.checkLogin(request)
    params = {
        'user_id': user_id,
        'page': request.POST.get('page', 1)
    }
    result = crawlerModel.crawlerList(params)
    return JsonResponse(result)


# 应用配置页
def crawlerConfig(request):
    user_id = userView.checkLogin(request)
    crawler_id = request.GET.get('crawler_id', None)
    result = {}
    if crawler_id is not None:
        result = crawlerModel.crawlerConfig(crawler_id=crawler_id, user_id=user_id)
    return render(request, 'crawler/config.html', result)


# 保存配置
def saveConfig(request):
    post = request.POST
    user_id = userView.checkLogin(request)

    # 不传ID就凉
    if post.get('name', None) is None or post.get('area', None) is None:
        result = 'error'
    else:
        post.user_id = user_id
        result = crawlerModel.saveCrawler(post)
    return JsonResponse({'status': result})

