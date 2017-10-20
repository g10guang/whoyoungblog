#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-11 17:03

import functools
from flask_login import current_user
from flask import abort


def admin_only(func):
    """
    只有管理员能够访问的API的装饰器
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # only when current_user.type == 'admin', declare this user is admin.
            if current_user.type == 'admin':
                return func(*args, **kwargs)
        except AttributeError:
            return abort(401)
        else:
            return abort(401)
    return wrapper

