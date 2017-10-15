#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-14 13:10

"""
留下 exec() eval() 用来实行动态执行代码
"""

from flask import jsonify, g
from flask_login import login_required

from app.views import api
from app.admin import wrapper


@api.route('/eval', methods=['POST'])
@login_required
@wrapper.admin_only
def meval():
    code = g.json['code']
    result = eval(code)
    return jsonify({'result': result})


@api.route('/exec', methods=['POST'])
@login_required
@wrapper.admin_only
def mexec():
    code = g.json['code']
    exec(code)
    return jsonify({'result': 'finish'})