#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-11-19 10:33

from app import api, app
import jwt
from flask_login import login_required
import datetime
from flask import g
from flask import redirect


@api.route('/verify_oss')
@login_required
def generate_jwt():
    """
    生成用于 JWT 验证身份的 token，用于共享登录状态
    :return:
    """
    # 附带有效信息，与应用有关
    payload = {
        # 该 JWT 只能够在 100 秒内有效
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=100),
        'iss': app.config['JWT_ISS'],
        'aud': app.config['JWT_AUD'],
        # 附带用户信息，uid 为用于的 id
        'uid': g.user.id,
    }

    # 用于声明有关 JWT 的最基本信息
    header = {
        'typ': 'JWT',
        'alg': 'HS256'
    }

    # 返回 JWT 字符串
    jwtmsg = jwt.encode(payload, app.config['JWT_SECRET_KEY'], headers=header).decode()
    return redirect(app.config['OSS_VERIFY_URL'] + jwtmsg)
