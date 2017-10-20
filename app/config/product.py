#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-10 18:23

from app.config.default import Config


class ProductConfig(Config):
    """
    产品配置类
    """
    DEBUG = False

    SERVER_NAME = 'whoyoung.me'

    REMEMBER_COOKIE_DOMAIN = '.whoyoung.me'

