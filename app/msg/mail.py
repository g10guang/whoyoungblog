#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-20 10:01

from flask_mail import Message
from app import mail


def send_mail(subject, recipient, html=None, body=None):
    """
    发送邮件
    :param recipient:收件人邮箱
    :param subject: 邮件 title
    :param html: 邮件中的信息
    :param body: 邮件内容
    :return:
    """
    msg = Message(subject, recipients=[recipient])
    msg.html = '<h1>你最近还好吗!!!</h1>'
    mail.send(msg)