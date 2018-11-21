# -*- coding: utf-8 -*-
from django.shortcuts import render


def index(request):
    return render(request, 'login.html')


def login():
    return render(request, 'login.html')
