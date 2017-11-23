#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-10 18:22

from app.config.default import Config


class DevelopConfig(Config):
    """
    开发环境中的配置类
    """
    DEBUG = True

    SERVER_NAME = 'hello.com:5000'

    REMEMBER_COOKIE_DOMAIN = '.hello.com'

    OSS_DOMAIN = 'oss.whoyoung.me'

    OSS_VERIFY_URL = '{domain}/jwt_verify?jwt='.format(domain=OSS_DOMAIN)