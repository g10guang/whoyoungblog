#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-13 08:46
# 提供对象存储
# 用于用户上传文件或者图片

import traceback

import gridfs
from bson.objectid import ObjectId
from flask import request, make_response, url_for
from flask_login import login_required, current_user

from app import mongo, fs_grid, is_grid
from app.store import store, STORE_DOMAIN
from app.tools import convert


@store.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Expose-Headers'] = 'Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'HEAD, OPTIONS, GET, POST, DELETE, PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Referer, Accept, Origin, User-Agent, X-Requested-With, Content-Type, withCredentials'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@store.route('/file')
def get_file_by_oid():
    """
    通过文件 id 查看文件
    :return:
    """
    oid = ObjectId(request.args['id'])
    try:
        with fs_grid.get(oid) as file:
            response = make_response(file.read())
            response.headers['Content-Type'] = file.content_type
            return response
    except gridfs.errors.NoFile:
        return 'File not found', 404


@store.route('/file/name')
def get_file():
    """
    通过文件名查看文件
    :return:
    """
    filename = request.args['filename']
    return mongo.send_file(filename)


@store.route('/file', methods=['POST'])
@login_required
def store_file():
    """
    上传文件
    :return:
    """
    try:
        file = request.files['file']
        oid = fs_grid.put(file, content_type=file.headers['Content-Type'], owner=current_user._id, filename=file.filename)
        url = convert.build_url(STORE_DOMAIN, url_for('store.get_file_by_oid', id=str(oid)))
        return url
    except (KeyError, TypeError):
        traceback.print_exc()
        return '-1'


@store.route('/image/name')
def get_image():
    """
    通过图片名字查找图片
    :return:
    """
    filename = request.args['filename']
    return mongo.send_file(filename, base='is')


@store.route('/image')
def get_image_by_oid():
    """
    通过图片的 id 寻找图片
    :return:
    """
    oid = ObjectId(request.args['id'])
    with is_grid.get(oid) as image:
        response = make_response(image.read())
        response.headers['Content-Type'] = image.content_type
        return response


@store.route('/image', methods=['POST'])
@login_required
def store_image():
    """
    上传图片
    :return:
    """
    try:
        image = request.files['image']
        oid = is_grid.put(image, content_type=image.headers['Content-Type'], owner=current_user._id, filename=image.filename)
        url = convert.build_url(STORE_DOMAIN, url_for('store.get_image_by_oid', id=str(oid)))
        return url
    except (KeyError, TypeError):
        traceback.print_exc()
        return '-1'
