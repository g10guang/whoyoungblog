#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-10 18:11


import os


def load_config():
    """
    加载配置文件
    :return:
    """
    MODE = os.environ.get('BLOG_MODE')
    try:
        if MODE == 'PRODUCT':
            # 在生产环境，将标准输入流输出流重定向到文件中
            import sys
            f = open('std.txt', 'w')
            sys.stderr = f
            sys.stdout = f
            from app.config.product import ProductConfig
            return ProductConfig
        else:
            from app.config.develop import DevelopConfig
            return DevelopConfig
    except ImportError:
        from app.config.default import Config
        return Config
