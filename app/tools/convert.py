#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-11 18:33

from flask import request
import pymongo
from app.tools import info


def convert_ObjectId2str(item):
    item['_id'] = str(item['_id'])
    return item


def paginate(items, page, size):
    """
    分页功能
    :param items:
    :param page:
    :param size:
    :return:
    """
    page = int(page)
    size = int(size)
    return items.skip((page - 1) * size).limit(size).sort('_id', pymongo.DESCENDING)


def build_url(server_name, url):
    return '{}{}'.format(server_name, url)


def is_author_format(author):
    """
    检查 author 字段是否符合格式
    用于 project 上传设置
    :return:
    """
    if not isinstance(author, list):
        return False
    for a in author:
        if len(a) != 2:
            return '-1'
        if 'name' in a and 'url' in a:
            if isinstance(a['name'], str) and isinstance(a['url'], str):
                continue
        return False
    return True


def is_like(item):
    client_ip = info.get_client_ip()
    item['isLiked'] = client_ip in item['likeIPs']
    return item


def make_list_element_unique(l):
    """
    处理 list 使得元素唯一
    :return:
    """
    return list(set(l))
