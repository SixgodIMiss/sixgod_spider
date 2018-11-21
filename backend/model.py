# -*- coding: utf-8 -*-
from django.db import models


class User(models.Model):
    id = models.Index
    name = models.CharField('名字', max_length=16)
    password = models.CharField('密码', max_length=32)
    auth = models.IntegerField('权限', max_length=1)
    register_time = models.DateTimeField('注册时间').auto_now_add

    class Meta:
        db_table = 'user'

