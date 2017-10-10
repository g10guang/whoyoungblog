#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-10 18:22

import os


class Config:
    """
    默认配置类
    """
    DEBUG = False

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

    MONGODB_DBNAME = 'whoyoungblog'

    MONGODB_HOST = os.environ.get('MONGODB_HOST', '127.0.0.1')

    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', '')

    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', '')

    MONGODB_PORT = os.environ.get('MONGODB_PORT', 27017)

    MONGODB_AUTH_MECHANISM = 'SCRAM-SHA-1'

    # declare what SERVER_NAME we use. This is for subdomain service.

    # OBJ_STORE_IMAGE_BASE = 'image'

    # flask-login token name
    REMEMBER_COOKIE_NAME = 'UserToken'
