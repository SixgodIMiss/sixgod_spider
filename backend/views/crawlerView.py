# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from backend.views import userView
from backend.models import crawlerModel


def index(request):
    logined = request.session.get('user_id', None)
    if logined is None:
        return HttpResponseRedirect('/login')
    return render(request, 'crawler/list.html')


def crawlerList(request):
    user_id = userView.checkLogin(request)
    result = crawlerModel.crawlerConfig(1)
    return JsonResponse({'uid': result})


def crawlerConfig(request):
    user_id = userView.checkLogin(request)
    post = request.POST
    crawler_id = post.get('crawler_id', None)
    if crawler_id is None or crawler_id == '':
        return render(request, 'crawler/config.html', {})
    else:
        if post.get('name', None) is None or post.get('area', None) is None:
            return render(request, 'error.html', {'error': '填写内容有误，请重填'})
        post['user_id'] = user_id

        crawlerModel.createCrawler(post)
        return render(request, 'index.html', {})
