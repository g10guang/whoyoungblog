#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-15 18:27

from flask import g, jsonify
from app.views import api
from app import mongo
from app.tools import convert, check


@api.route('/search_articles')
def search_articles():
    keyword = g.args['keyword']
    page = g.args.get('page', 1)
    size = g.args.get('size', 20)
    # db.articles.find({$text: {$search: 'launch.json'}}).pretty()
    result = convert.paginate(
        mongo.db.articles.find({'$text': {'$search': keyword}, 'status': 'published'},
                               {'_id': False, 'content': False, 'markdown': False, 'likeIPs': False, 'comments': False, 'status': False}), page, size)
    articles = list(result)
    # 对 title 和 intro 进行复查，因为 MongoDB 全文检索对中文支持不好
    if check.check_str_contain_chinese(keyword):
        result_2 = convert.paginate(mongo.db.articles.find({'$or': [{'title': {'$regex': keyword}}, {'intro': {'$regex': keyword}}]},
                                                           {'_id': False, 'content': False, 'markdown': False, 'likeIPs': False, 'comments': False, 'status': False}), page, size)
        id_set = {item['id'] for item in articles}
        for item in result_2:
            if item['id'] not in id_set:
                articles.append(item)
    # # 查询出来结果需要去重
    return jsonify({'articles': articles})



