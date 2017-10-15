#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-14 14:59
# description: 消息处理模块

from app import mongo
import uuid
from app.tools import timeformat

# 以下数据库连接用于调试
# from pymongo import MongoClient
#
#
# client = MongoClient()
#
# db = client.whoyoungblog


def store_msg(sender_id, receiver_id, content):
    """
    发送消息，将消息存储进数据库
    :param sender_id: 发送人id
    :param receiver_id: 接受者id
    :param content: 消息内容
    :return: True 插入成功；False 数据库更新失败
    """
    count = mongo.db.admins.find({'id': {'$in': [sender_id, receiver_id]}}).count()
    if count != 2:
        # sender_id == receiver_id 或者是不存在 sender_id 或者 receiver_id
        return False
    msgid = uuid.uuid4().hex
    now_str = timeformat.get_now_strformat()
    # 每发布一条消息需要经过两次查库操作
    try:
        # 1. 发送人发送消息先插入
        mongo.db.msgs.update_one({'userId': sender_id},
                             {'$push': {'msg': {'other': receiver_id, 'id': msgid, 'time': now_str, 'content': content, 'hasRead': True, 'isSender': True}}})
        # 2. 接受者消息队列插入
        mongo.db.msgs.update_one({'userId': receiver_id},
                             {'$push': {'msg': {'other': sender_id, 'id': msgid, 'time': now_str, 'content': content, 'hasRead': False, 'isSender': False}}})
    except Exception:
        raise
    else:
        return True


def query_unread_msg(user_id):
    """
    查询某个用户的未读消息
    :param user_id: 查询人的 id
    :return:
    """
    # 查询所有未读的消息
    result = mongo.db.msgs.aggregate([
        {'$match': {'userId': user_id}},
        {'$project': {
            'msg': {
                '$filter': {'input': '$msg', 'as': 'msg', 'cond': {'$eq': ['$$msg.hasRead', False]}}
            },
            '_id': False
        }
        }
        ])
    unread_msgs = next(result)
    # 把所有未读的消息更新为已读消息
    # 由于目前 mongo 还不支持对数组过滤更新，但官方文档说明了 mongo3.6 支持数组过滤更新，所以暂时只有写更新操作
    # 此方法比较低效，需要在 mongodb 3.6 出台后修改该代码片段
    for item in unread_msgs['msg']:
        mongo.db.msgs.update({'userId': user_id, 'msg.id': item['id']}, {'$set': {'msg.$.hasRead': True}})
    return unread_msgs


def withdraw_msg(msg_id):
    """
    撤回消息
    :param msg_id:
    :return:
    """
    result = mongo.db.msgs.update_many({'msg.id': msg_id}, {'$pull': {'msg': {'id': msg_id}}}, False)
    return result

