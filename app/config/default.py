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

    # 设置邮箱
    MAIL_SERVER = 'smtp.exmail.qq.com'

    MAIL_PORT = 465

    MAIL_USE_SSL = True

    MAIL_USE_TLS = False

    MAIL_USERNAME = os.environ.get('BLOG_MAIL_USERNAME', 'admin@whoyoung.me')

    MAIL_PASSWORD = os.environ.get('BLOG_MAIL_PASSWORD', 'Whoyoung734')

    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    MAIL_DEBUG = False      # 关闭 flask-mail 中连接中产生的大量日志
