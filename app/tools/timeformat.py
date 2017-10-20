#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-11 17:28

import datetime


def get_now_strformat():
    """
    返回时间格式，如 2017-10-1 10:10
    :return:
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


def create_time_id():
    """
    产生与时间相关的 id
    :return:
    """