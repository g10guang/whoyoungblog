#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-11 11:08

import pymongo
import uuid
from flask import request, jsonify, g, abort

from app import mongo
from app.tools import convert, timeformat
from app.views import api, RANDOM_IMG_DEFAULT_URL
from app.tools import info
from app.tools import articletool


@api.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Expose-Headers'] = 'Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Referer, Accept, Origin, User-Agent, X-Requested-With, Content-Type, withCredentials'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@api.route('/get_articles_intro')
def get_articles_intro():
    """
    博客主页请求的数据
    :return:
    """
    page = g.args.get('page', 1)
    size = g.args.get('size', 10)

    cursor = convert.paginate(mongo.db.articles.find({'status': 'published'},
                                                     {'_id': False, 'content': False, 'status': False, 'markdown': False, 'comments': False}), page, size)
    articles = list(cursor)
    for item in articles:
        convert.is_like(item)
    return jsonify(articles)


@api.route('/get_article')
def get_article():
    uid = g.args['id']
    article = mongo.db.articles.find_one_and_update({'id': uid, 'status': 'published'}, {'$inc': {'browseNumber': 1}}, {'_id': False, 'status': False, 'markdown': False})
    if article is None:
        return abort(404)
    convert.is_like(article)
    return jsonify(article)


@api.route('/get_tags')
def get_tags():
    """
    查找所有标签
    :return:
    """
    result = mongo.db.articles.distinct('tags', {'status': 'published'})
    return jsonify({'name': '标签', 'lists': list(result)})


@api.route('/tags')
def get_articles_by_tag():
    page = g.args.get('page', 1)
    size = g.args.size('size', 10)
    tag = g.args['tag']
    result = convert.paginate(mongo.db.articles.find({'tags': {'$elemMatch': {'name': tag}}, 'status': 'published'},
                                                     {'_id': False, 'markdown': False, 'status': False}), page, size)
    articles = list(result)
    return jsonify(articles)


@api.route('/get_random_img_url')
def get_random_img_url():
    """
    前段请求随机的图片 url
    :return:
    """
    result = mongo.db.images.aggregate([{'$sample': {'size': 1}}])
    return jsonify({'url': result.next().get('url', RANDOM_IMG_DEFAULT_URL)})


@api.route('/get_hot_articles')
def get_hot_articles():
    """
    通过点赞数量排序热门文章
    :return:
    """
    page = g.args.get('page', 1)
    size = g.args.get('size', 10)
    result = convert.paginate(mongo.db.articles.find({'status': 'published'}, {'_id': False, 'title': True, 'id': True, 'likes': True}),
                              page, size).sort('likes', pymongo.DESCENDING)
    articles = [{'title': item['title'], 'id': item['id']} for item in result]
    return jsonify({'name': '墨点', 'lists': articles})


@api.route('/get_projects_intro')
def get_projects_intro():
    page = g.args.get('page', 1)
    size = g.args.get('size', 10)
    result = convert.paginate(mongo.db.projects.find({'isDel': False}, {'_id': False, 'isDel': False}), page, size)
    projects = list(result)
    return jsonify(projects)


@api.route('/get_hot_projects')
def get_hot_projects():
    # TODO 后面需要进行修改，目前没有确定热门标准
    result = mongo.db.projects.find({})
    projects = list()
    for item in result:
        projects.append({'title': item['name'], 'url': item['projectURL']})
    return jsonify({'name': '墨点', 'lists': projects})


@api.route('/get_authors_info')
def get_authors_info():
    """
    请求作者信息
    :return:
    """
    result = mongo.db.admins.find({}, {'_id': False, 'cryptPassword': False})
    authors = {}
    for item in result:
        item['articles'] = list()
        item['tags'] = list()
        authors[item['username']] = item
    # 查找该作者的文章
    articles = mongo.db.articles.find({'author.username': {'$in': list(authors)}, 'status': 'published'},
                                       {'_id': False, 'title': True, 'author': True, 'id': True, 'tags': True})
    for item in articles:
        author_name = item['author']['username']
        authors[author_name]['articles'].append({'title': item['title'], 'id': item['id']})
        for t in item['tags']:
            if t not in authors[author_name]['tags']:
                authors[author_name]['tags'].append(t)
    return jsonify(authors)


@api.route('/get_project')
def get_project():
    uid = g.args['id']
    project = mongo.db.projects.find_one_and_update({'id': uid, 'isDel': False}, {'$inc': {'browseNumber': 1}},
                                                    {'_id': False, 'isDel': False},
                                                    return_document=pymongo.ReturnDocument.AFTER)
    return jsonify({'project': project})


@api.route('/get_tag_articles')
def get_tag_articles():
    # 得到所有已发布文章的标签
    result = mongo.db.articles.distinct('tags', {'status': 'published'})
    articles = list()
    for item in result:
        posts = {'name': item['name'], 'id': item['id'], 'articles': list()}
        tmp = convert.paginate(mongo.db.articles.find({'status': 'published', 'tags.name': item['name']}, {'_id': False, 'title': True, 'id': True}), 1, 4)
        for item in tmp:
            posts['articles'].append({'title': item['title'], 'id': item['id']})
        articles.append(posts)
    return jsonify(articles)


@api.route('/get_header_nav_info')
def get_header_nav_info():
    navinfo = mongo.db.navinfo.find_one({}, {'_id': False})
    return jsonify(navinfo)


@api.route('/like_article', methods=['POST'])
def like_article():
    """
    点赞文章功能
    :return:
    """
    uid = g.args['id']
    client_ip = info.get_client_ip()
    # 如果文章存在且未被该 ip 点赞，则点赞
    result = mongo.db.articles.update_one({'id': uid, 'likeIPs': {'$ne': client_ip}},
                                          {'$addToSet': {'likeIPs': client_ip}, '$inc': {'likeNumber': 1}}, False)
    # status == 1 点赞成功，status == 0 文章已被删除
    return jsonify({'status': 1 if result.raw_result['updatedExisting'] else 0})


@api.route('/publish_comment', methods=['POST'])
def publish_comment():
    """
    评论文章功能
    :return:
    """
    article_id = g.json['id']      # 文章 id
    new_comment = g.json['comment']
    title = new_comment['title']
    content = new_comment['content']
    email = new_comment['email']
    username = new_comment['username']
    uid = uuid.uuid4().hex      # 评论的 id
    user_id = uuid.uuid4().hex  # 评论用户的 id
    comment_id = new_comment['commentId']
    now_str = timeformat.get_now_strformat()
    # 待插进数据库的 comment
    comment = {'id': uid, 'title': title, 'createdTime': now_str, 'lastModifiedTime': now_str, 'content': content,
               'from': {'userId': user_id, 'username': username, 'email': email}}
    # 判断是评论文章还是回复评论
    if not comment_id:
        # 评论文章
        comment['childrenComments'] = []
        # 将新评论放在首位
        result = mongo.db.articles.update_one({'id': article_id, 'status': 'published'}, {'$push': {'comments': {'$each': [comment], '$position': 0}}}, False)
    else:
        # 回复评论
        article_comment = mongo.db.articles.find_one({'id': article_id, 'status': 'published'}, {'_id': False, 'comments': True})
        # 寻找 target 中的 username userId email 等信息
        tmp = articletool.find_from_tag_by_comment_id(comment_id, article_comment['comments'])
        if not tmp:
            # 参数错误
            abort(400)
        from_tag, top_comment_id = tmp
        if not from_tag:
            # 回复的评论已经不存在
            abort(404)
        target_user_id = from_tag['userId']
        target_username = from_tag['username']
        target_email = from_tag['email']
        comment['target'] = {'commentId': comment_id, 'userId': target_user_id, 'username': target_username, 'email': target_email}
        result = mongo.db.articles.update_one({'id': article_id, 'status': 'published', 'comments.id': top_comment_id}, {'$push': {'comments.$.childrenComments': comment}})
    return jsonify({'status': 1 if result.raw_result['updatedExisting'] else 0})


@api.route('/get_comments')
def get_comments():
    article_id = g.args['id']
    article = mongo.db.articles.find_one({'id': article_id}, {'_id': False, 'comments': True})
    return jsonify({'comments': article['comments']})