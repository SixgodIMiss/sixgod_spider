# -*- coding: utf-8 -*-
import os, sys, psutil, time, platform, re, socket, uuid
import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from psutil import net_if_addrs



# 当前只考虑Windows
def is_windows():
    plat = platform.system()
    if 'Windows' in plat:
        return True
    else:
        return False


def sys_info():
    return {
        'cpu': cpu_info(),
        'memory': memory_info(),
        'disk': disk_info()
    }


# MB
def memory_info():
    memory = psutil.virtual_memory()
    return {
        'total': memory.total / MEMORY_CONVERT,  # MB 总量
        'available': memory.available / MEMORY_CONVERT,  # 可用
        'percent': memory.percent,  # 使用率
        'used': memory.used / MEMORY_CONVERT,  # 已用
        'free': memory.free / MEMORY_CONVERT,  # 剩余
    }


def cpu_info():
    return {
        'core': psutil.cpu_count(),  # 核心数
        'percent': psutil.cpu_percent(0),  # 使用率,
        'per_percent': psutil.cpu_percent(percpu=True)
    }


def disk_info():
    return psutil.disk_partitions()
    # return psutil.disk_usage('C:')


def user_info():
    return psutil.users()


# 获取任务文件
def read_task_file():
    task_files = []
    files = os.listdir(PROJECT_PATH)
    for f in files:
        path = os.path.join(PROJECT_PATH, f)
        if os.path.isdir(path) or 'task' not in path:
            continue
        else:
            task_files.append(path)

    return task_files


# 获取当前所有活动进程
def process():
    pids = psutil.pids()
    processes = []
    for pid in pids:
        try:
            p = psutil.Process(pid)
            if p.status() == 'running':
                processes.append(p)
        except Exception as e:
            print(e)
    return processes


# 获取正在运行爬虫的省份 即应该运行有哪些爬虫
def task_province():
    processes = process()  # 当前所有活动进程
    task_files = read_task_file()  # 爬虫任务脚本
    result = []
    for p in processes:
        try:
            if p.status() == 'running':
                shell = p.cmdline()
                for sh in shell:
                    # print(sh)
                    for task in task_files:
                        filename = os.path.basename(task)
                        if filename in sh:
                            with open(task, 'r+') as fp:
                                line = fp.read().decode('utf-8')
                                partern = re.compile('province_list = \[(.*)\]')  # 获取任务启动了哪几个省
                                provinces = partern.findall(line)
                                if provinces:
                                    result = provinces[0]
        except Exception as e:
            # print(e)
            pass

    return result


def get_ip():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_mac():
    node = uuid.getnode()
    address = hex(node)[2:]
    print(node)
    return '-'.join(address[i:i+2] for i in range(0, len(address), 2))


MEMORY_CONVERT = 1048576  # 1024*1024
if is_windows():
    PROJECT_PATH = 'E:/python/slf_spider/'
else:
    PROJECT_PATH = ''

# get_mac()
