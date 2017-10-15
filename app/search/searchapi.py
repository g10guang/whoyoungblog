#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-15 18:27

from flask import g, jsonify
from app.views import api
from app import mongo
from app.tools import convert


@api.route('/search_articles')
def search_articles():
    keyword = g.args['keyword']
    page = g.args.get('page', 1)
    size = g.args.get('size', 20)
    # db.articles.find({$text: {$search: 'launch.json'}}).pretty()
    result = convert.paginate(
        mongo.db.articles.find({'$text': {'$search': keyword}, 'status': 'published'},
                               {'_id': False, 'content': False, 'markdown': False, 'likeIPs': False, 'comments': False}), page, size)
    articles = list(result)
    return jsonify({'articles': articles})