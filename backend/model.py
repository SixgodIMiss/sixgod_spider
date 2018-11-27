# -*- coding: utf-8 -*-
from django.db import models
import datetime


# 用户
class User(models.Model):
    id = models.Index
    name = models.CharField('名字', max_length=16)
    password = models.CharField('密码', max_length=32)
    auth = models.IntegerField('权限', max_length=1)
    register_time = models.DateTimeField('注册时间', default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        db_table = 'user'

# 应用配置
class CrawlerConfig(models.Model):
    id = models.Index
    name = models.CharField('爬虫应用名')
    user = models.ForeignKey(User)  # 创建者
    province = models.CharField('省')
    city = models.CharField('市')
    spiders = models.CharField('用到的爬虫程序ID')
    create_time = models.DateTimeField('创建时间', default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_time = models.DateTimeField('更新时间', default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        db_table = 'crawler_config'

# 运行任务
class Task(models.Model):
    id = models.Index
    status = models.CharField('运行状态')  # stop stopping running starting
    start = models.DateTimeField('启动时间')  # 上一次
    end = models.DateTimeField('关闭时间')  # 上一次
    pid = models.IntegerField('进程ID')
    create_time = models.DateTimeField('创建时间', default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        db_table = 'task'

# 爬虫应用
class Crawler(models.Model):
    id = models.Index
    config = models.ForeignKey(CrawlerConfig)  # 配置记录ID
    task = models.ForeignKey(Task)  # 运行任务
    valid = models.IntegerField(default=1)  # 是否1有效, 2无
    create_time = models.DateTimeField('创建时间', default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Meta:
        db_table = 'crawler'



