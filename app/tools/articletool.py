#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-15 12:53


def find_from_tag_by_comment_id(comment_id, comment_list):
    """
    通过评论 id 寻找 from 标签，查看发布该评论的作者信息
    :param comment_id:
    :param comment_list: 顶级评论 list
    :return: from 标签；如果找不到则返回 None
    """
    for comment in comment_list:
        if comment['id'] == comment_id:
            return comment['from'], comment['id']
        for child in comment['childrenComments']:
            if child['id'] == comment_id:
                return child['from'], comment['id']
    return None