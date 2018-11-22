# -*- coding: utf-8 -*-
from backend.model import User


# 查询用户
def getUser(uid, name=True):
    if name:
        return User.objects.get(id=uid).name
    else:
        return User.objects.get(id=uid)


# 登录验证
def validation(name=None, pwd=None):
    result = {
        'status': False,
        'user_name': '',
        'user_id': '',
        'msg': 0
    }
    if name is None or pwd is None:
        result['msg'] = 1
    else:
        data = User.objects.filter(name=name).values()
        if len(data):
            password = data[0]['password']
            if pwd == password:
                result['status'] = True
                result['user_id'] = data[0]['id']
                result['user_name'] = data[0]['name']
            else:
                result['msg'] = 2
        else:
            result['msg'] = 3

    return result

