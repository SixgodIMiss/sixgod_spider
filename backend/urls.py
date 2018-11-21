# -*- coding: utf-8 -*-
from django.conf.urls import url
from view import spiderView, userView

backend_urlpatterns = [
    url(r'^$', spiderView.index, name='index'),
    url(r'^index/$', spiderView.index, name='index'),
    url(r'^login/$', userView.login, name='login'),
    url(r'^signIn/$', userView.signIn, name='signIn')
]

