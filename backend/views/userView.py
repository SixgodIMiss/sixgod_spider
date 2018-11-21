# -*- coding: utf-8 -*-
from django.shortcuts import render


def login(request):
    return render(request, 'login.html')


def signIn(request):
    post = request.POST

