# -*- coding: utf-8 -*-
from django.conf.urls import url
from backend.views import spiderView, userView, crawlerView, dataView, logView

backend_urlpatterns = [
    url(r'^$', crawlerView.index, name='index'),
    url(r'^index/$', crawlerView.index, name='index'),
    url(r'^login/$', userView.login, name='login'),
    url(r'^signIn/$', userView.signIn, name='signIn'),
    url(r'^logout/$', userView.logout, name='logout'),

    url(r'^crawlerList/$', crawlerView.crawlerList, name='crawlerList'),
    url(r'^crawlerConfig/$', crawlerView.crawlerConfig, name='crawlerConfig'),
    url(r'^crawlerSave/$', crawlerView.crawlerSave, name='crawlerSave'),
    url(r'^crawlerInfo/$', crawlerView.crawlerInfo, name='crawlerInfo'),
    url(r'^crawlerHandler/$', crawlerView.handler, name='crawlerHandler'),
    url(r'^crawlerTask/$', crawlerView.taskInfo, name='crawlerTask'),
    url(r'^crawlerStatus/$', crawlerView.checkStatus, name='crawlerStatus'),

    url(r'^spiderIndex/$', spiderView.index, name='spiderIndex'),
    url(r'^spiderList/$', spiderView.spiderList, name='spiderList'),
    url(r'^spiderConfig/$', spiderView.config, name='spiderConfig'),
    url(r'^spiderSave/$', spiderView.save, name='spiderSave'),

    url(r'^data/timeline$', dataView.timeline, name='timeline'),
    url(r'^data/list', dataView.dataList, name='dataList'),

    url(r'^data/list', dataView.dataList, name='dataList'),
    url(r'^data/transfer', dataView.transfer, name='dataTransfer'),

    url(r'^log/operate$', logView.operateList, name='logOperate')
]

