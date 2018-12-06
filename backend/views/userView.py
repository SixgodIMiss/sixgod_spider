# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from backend.models import userModel


# 登录页面
def login(request):
    return render(request, 'login.html')


# 登录判断
def signIn(request):
    post = request.POST
    info = userModel.validation(post['name'], post['password'])
    if info['status'] is True:
        request.session['user_id'] = info['user_id']
        request.session['user_name'] = info['user_name']

        remember = post.get('remember', None)
        if remember == 'on':
            request.session.set_expiry(86400)
        else:
            request.session.set_expiry(7200)
    return JsonResponse(info)


# 验证登录
def checkLogin(request):
    user_id = request.session.get('user_id', None)
    if user_id is None:
        return HttpResponseRedirect('/login')
    else:
        return user_id


def logout(request):
    print(request.session)
    return HttpResponseRedirect('/login')
