# -*- coding: utf-8 -*-
import datetime
from backend.model import Crawler, CrawlerConfig, Task, Spider, RunLog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 插入日志
def insert(params):
    insert = RunLog.objects.create(task_id=params['task_id'], crawler_id=params['crawler_id'], execute=
                                   params['execute'], result=params['result'], remark=params['remark'])

    if insert:
        return True
    else:
        return False

