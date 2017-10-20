#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-20 18:58

from app import app
from flask import Blueprint

store = Blueprint('store', 'store', subdomain='store')


STORE_DOMAIN = 'store.{}'.format(app.config['SERVER_NAME'])