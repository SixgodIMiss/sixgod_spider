# -*- coding: utf-8 -*-
from django.conf.urls import url
from view import spiderView

backend_urlpatterns = [
    url(r'^$', spiderView.index, name='index'),
    url(r'^index/$', spiderView.index, name='index')
]

