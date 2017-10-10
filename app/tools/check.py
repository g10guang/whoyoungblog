#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-06 20:14


USER_STATUS_SET = {'frozen', 'deleted', 'normal'}

ARTICLE_STATUS_SET = {'craft', 'deleted', 'published'}


def verify_user_status(status):
    """
    用户状态：
    1. frozen   冻结
    2. deleted  删除
    3. normal   正常
    :return: 
    """
    return status in USER_STATUS_SET


def verify_article_status(status):
    """
    文章状态：
    1. craft    草稿
    2. deleted  删除
    3. published    发布
    :param status: 
    :return: 
    """
    return status in ARTICLE_STATUS_SET