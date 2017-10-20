#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-15 14:32

from app.views import api
from flask_login import login_required
from flask import g, jsonify

from app.msg import msgtools
from app.msg import mail


@api.route('/get_unread_msg')
@login_required
def get_msg():
    unread_msg = msgtools.query_unread_msg(g.user.id)
    return jsonify(unread_msg)


@api.route('/get_msg_before_msgid')
def get_msg_before_msgid():
    msgs = msgtools.more_msg_before_msg_id(g.user.id, g.args.get('msgid', None), g.args.get('size', 20))
    return jsonify(msgs)


@api.route('/send_mail')
def send_mail():
    mail.send_mail('A mail from g10guang', 'g10guang@foxmail.com')
    return 'ok'