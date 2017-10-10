#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-11 18:33

from flask import make_response
import pymongo
import functools


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


def convert_article_format(article):
    """
    转换 article 格式为前段需要格式
    :param article:
    :return:
    """
    parse_time_format(article)
    # item['articleURL'] = url_for('get_article', uid=item['id'])
    # tags = item['tags']
    # tmp = list()
    # for t in tags:
    #     tmp.append({'title': t, 'url': url_for('get_articles_by_tag', tag=t)})
    # item['tags'] = tmp
    return article


def convert_user_format(user):
    user['signUpTime'] = user['signUpTime'].strftime('%Y-%m-%d %H:%M')


def parse_time_format(item):
    """
    转化时间格式
    :param item:
    :return:
    """
    item['createdTime'] = item['createdTime'].strftime('%Y-%m-%d %H:%M')


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


def mock_response_header_for_test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        response = make_response(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
