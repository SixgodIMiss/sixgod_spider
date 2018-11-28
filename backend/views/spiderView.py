# -*- coding: utf-8 -*-
import os
import subprocess
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from backend.views import userView
from backend.models import spiderModel


def index(request):
    userView.checkLogin(request)
    return render(request, 'spider/list.html', {})


def spiderList(request):
    user_id = userView.checkLogin(request)
    post = request.POST
    params = {
        'page': post.get('cPage', 1),
        'size': post.get('pSize', 20),
        'name': post.get('name', None)
    }
    result = spiderModel.spiderList(params)
    return JsonResponse(result)


def config(request):
    userView.checkLogin(request)
    return render(request, 'spider/config.html', {})


def save(request):
    userView.checkLogin(request)
    post = request.POST
    params = {
        'name': post.get('name', ''),
        'province': post.get('province', ''),
        'city': post.get('city', '')
    }
    result = {
        'status': 'fail',
        'msg': ''
    }

    # 调用子进程查看scrapy列表
    scrapy_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/spider')
    scrapy_run = subprocess.Popen('scrapy list', cwd=scrapy_path, stdout=subprocess.PIPE)
    scrapy_run.wait()
    scrapy_list = scrapy_run.stdout.readlines()
    lists = list(map(lambda x: x.replace('\n', ''), scrapy_list))

    if params['name'] not in lists:
        result['msg'] = '名称未找到'
    else:
        if spiderModel.save(params):
            result['status'] = 'success'
        else:
            result['msg'] = '添加失败'

    return JsonResponse(result)
