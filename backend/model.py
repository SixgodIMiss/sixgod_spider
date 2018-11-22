# -*- coding: utf-8 -*-
from django.db import models


# 用户
class User(models.Model):
    id = models.Index
    name = models.CharField('名字', max_length=16)
    password = models.CharField('密码', max_length=32)
    auth = models.IntegerField('权限', max_length=1)
    register_time = models.DateTimeField('注册时间').auto_now_add

    class Meta:
        db_table = 'user'


# 应用配置
class CrawlerConfig(models.Model):
    id = models.Index
    name = models.CharField('爬虫应用名')
    user_id = models.ForeignKey(User)  # 创建者
    area = models.CharField('地区')
    spiders = models.CharField('用到的爬虫程序ID')
    create_time = models.DateTimeField('创建时间')
    update_time = models.DateTimeField('更新时间')

    class Meta:
        db_table = 'crawler_config'


# 爬虫应用
class Crawler(models.Model):
    id = models.Index
    config = models.ForeignKey(CrawlerConfig)  # 配置记录ID
    valid = models.IntegerField(default=1)  # 是否1有效, 2无
    create_time = models.DateTimeField('创建时间')

    class Meta:
        db_table = 'crawler'


# 运行任务
class Task(models.Model):
    id = models.Index
    crawler_id = models.ForeignKey(Crawler)  # 爬虫应用
    status = models.CharField('运行状态')  # stop stopping running starting
    start = models.DateTimeField('启动时间')
    end = models.DateTimeField('关闭时间')
    pid = models.IntegerField('进程ID')

    class Meta:
        db_table = 'task'
