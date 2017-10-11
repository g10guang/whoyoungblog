#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-11 18:33

from flask import request
import pymongo


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
    if isinstance(page, str):
        page = int(page)
    if isinstance(size, str):
        size = int(size)
    return items.skip((page - 1) * size).limit(size).sort('_id', pymongo.DESCENDING)


def build_url(server_name, url):
    return '{}{}'.format(server_name, url)


def is_navinfo_format(navinfo) -> bool:
    """
    >>> is_navinfo_format({
        "homeTitle": "简",
        "navList": {
            "home": {
                "title": "字里行间",
                "text": "原谅我放荡不羁爱自由"
            },
            "projects": {
                "title": "字迹",
                "text": "存在"
            },
            "tags": {
                "title": "标签",
                "text": ""
            },
            "authors": {
                "title": "执笔",
                "text": "写尽"
            }
        }
    })
    True
    检验数据格式是否符合 navinfo 导航需要格式
    :param navinfo:
    :return:
    """
    navlist = ['home', 'projects', 'authors']
    if navinfo and 'homeTitle' in navinfo:
        if 'navList' in navinfo:
            for item in navlist:
                if item not in navinfo['navList']:
                    return False
                if 'title' not in navinfo['navList'][item] or 'text' not in navinfo['navList'][item]:
                    return False
                if not isinstance(navinfo['navList'][item]['title'], str) or not isinstance(navinfo['navList'][item]['text'], str):
                    return False
            return True


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


def is_like(items):
    client_ip = request.environ['REMOTE_ADDR']
    for item in items:
        item['isLiked'] = client_ip in item['likeIPs']
    return items
