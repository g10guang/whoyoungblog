#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-29 14:47

import random
import hashlib

__choices = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def create_salt(length=10):
    """
    生成随机序列当盐
    :param length: 盐的长度
    :return:
    """
    return ''.join(random.choice(__choices) for _ in range(length))


def generate_password(psw, salt):
    """
   使用 md5 算法加密
   :return:
   """
    md5 = hashlib.md5()
    md5.update('{}{}'.format(salt, psw).encode())
    return md5.hexdigest()


if __name__ == '__main__':
    salt = create_salt()
    psw = 'workhard'
    l = []
    for _ in range(10):
        m = hashlib.md5()
        m.update(salt.encode())
        m.update(psw.encode())
        l.append(m.hexdigest())
    print(l)
    print(salt)