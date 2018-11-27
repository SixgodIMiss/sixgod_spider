# -*- coding: utf-8 -*-
from django.conf.urls import url
from backend.views import spiderView, userView, crawlerView

backend_urlpatterns = [
    url(r'^$', crawlerView.index, name='index'),
    url(r'^index/$', crawlerView.index, name='index'),
    url(r'^login/$', userView.login, name='login'),
    url(r'^signIn/$', userView.signIn, name='signIn'),

    url(r'^crawlerList/$', crawlerView.crawlerList, name='crawlerList'),
    url(r'^crawlerConfig/$', crawlerView.crawlerConfig, name='crawlerConfig'),
    url(r'^saveConfig/$', crawlerView.saveConfig, name='saveConfig'),
    url(r'^crawlerInfo/$', crawlerView.saveConfig, name='crawlerInfo'),
    url(r'^crawlerHandler/$', crawlerView.handler, name='crawlerHandler'),
]

