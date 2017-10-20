#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-14 14:59
# description: 消息处理模块

from app import mongo
from bson.objectid import ObjectId
from app.tools import timeformat


# 以下数据库连接用于调试
# from pymongo import MongoClient
#
# client = MongoClient()
#
# db = client.whoyoungblog


def store_msg(receiver_id, content):
    """
    发送消息，将消息存储进数据库
    :param receiver_id: 接受者id
    :param content: 消息内容
    :return: True 插入成功；False 数据库更新失败
    """
    receiver = mongo.db.admins.find({'id': receiver_id})
    if not receiver:
        # receiver 不存在
        return False
    msgid = ObjectId()      # 生成唯一 id
    now_str = timeformat.get_now_strformat()
    # 每发布一条消息需要经过两次查库操作
    try:
        # 1. 接受者消息队列插入
        mongo.db.msgs.update_one({'userId': receiver_id},
                             {'$push': {'msg': {'id': msgid, 'time': now_str, 'content': content, 'hasRead': False}}})
    except Exception:
        raise
    else:
        return True


def query_unread_msg(user_id):
    """
    查询某个用户的未读消息
    如果 user_id 不存在会抛出异常
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
        item['id'] = str(item['id'])    # 将 ObjectId 转化为 str
    return unread_msgs


def withdraw_msg(msg_id):
    """
    撤回消息
    :param msg_id:
    :return:
    """
    oid = ObjectId(msg_id)
    result = mongo.db.msgs.update_many({'msg.id': oid}, {'$pull': {'msg': {'id': oid}}}, False)
    return result


def more_msg_before_msg_id(user_id, msg_id, size):
    """
    查询某条信息后的更多通知
    :param user_id: 用户 id
    :param msg_id: 消息 id
    :param size: 消息数目
    :return:
    """
    # msg 为空，则用户是从没有未读消息，需要查看更多的消息
    if msg_id:
        oid = ObjectId(msg_id)
        # result = db.msgs.find({'userId': user_id, 'msg.id': {'$lt': oid}}, {'_id': False, 'msg': {'$slice': -size}})
        result = mongo.db.msgs.aggregate([
            {'$match': {'userId': user_id}},
            {'$project': {
                'msg': {
                    '$slice': [
                        {'$filter': {'input': '$msg', 'as': 'msg', 'cond': {'$lt': ['$$msg.id', oid]}}}, -2
                    ]
                },
                '_id': False,
            }
            }
        ])
    else:
        result = mongo.db.msgs.find({'userId': user_id}, {'_id': False, 'msg': {'$slice': -size}})
    msgs = list(result)[0]
    for item in msgs['msg']:
        item['id'] = str(item['id'])
        if not item['hasRead']:
            # 更新未读状态
            mongo.db.msgs.update({'userId': user_id, 'msg.id': item['id']}, {'$set': {'msg.$.hasRead': True}})
    return msgs


if __name__ == '__main__':
    store_msg('wuyiqing', '你有一条未读消息5')
    # unread_msg = query_unread_msg('wuyi')
    # print(unread_msg)
    # withdraw_msg('59e93e25461725474caef6c9')

    # msgs = more_msg_before_msg_id('wuyiqing', '59e93e0b461725472a13f8f6', 2)
    # print(msgs)