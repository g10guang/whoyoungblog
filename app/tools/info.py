#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-12 18:20

from flask import request
import os


BLOG_MODE = os.environ.get('BLOG_MODE')

# 有服务器环境和本地运行环境不一致，所以部分功能代码实现不一样
if BLOG_MODE == 'PRODUCT':
    get_client_ip = lambda : request.headers['X-Real-IP']
else:
    get_client_ip = lambda : request.environ['REMOTE_ADDR']