#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-10-06 20:14
# 将数据插入数据库之前应该确保数据格式的正确

import re

USER_STATUS_SET = {'frozen', 'deleted', 'normal'}

ARTICLE_STATUS_SET = {'draft', 'deleted', 'published'}

EMAIL_REGEX = r'[^@]+@[^@]+\.[^@]+'


def verify_user_status(status):
    """
    用户状态：
    1. frozen   冻结
    2. deleted  删除
    3. normal   正常
    :return: 
    """
    return status in USER_STATUS_SET


def verify_article_status(status):
    """
    文章状态：
    1. craft    草稿
    2. deleted  删除
    3. published    发布
    :param status: 
    :return: 
    """
    return status in ARTICLE_STATUS_SET


def verify_navinfo_format(navinfo) -> bool:
    """
    >>> verify_navinfo_format({
        "homeTitle": "简",
        "navList": {
            "home": {
                "title": "字里行间",
                "text": "原谅我放荡不羁爱自由"
            },
            "projects": {
                "title": "字迹",
                "text": "存在"
            },
            "tags": {
                "title": "标签",
                "text": ""
            },
            "authors": {
                "title": "执笔",
                "text": "写尽"
            }
        }
    })
    True
    检验数据格式是否符合 navinfo 导航需要格式
    :param navinfo:
    :return:
    """
    navlist = ['home', 'projects', 'authors']
    if navinfo and 'homeTitle' in navinfo:
        if 'navList' in navinfo:
            for item in navlist:
                if item not in navinfo['navList']:
                    return False
                if 'title' not in navinfo['navList'][item] or 'text' not in navinfo['navList'][item]:
                    return False
                if not isinstance(navinfo['navList'][item]['title'], str) or not isinstance(
                        navinfo['navList'][item]['text'], str):
                    return False
            return True


def verify_article_format(article):
    """
    检查格式是否符合 article 数据格式
    {
        "_id" : ObjectId("59b8f546461725635e250d4f"),
        "tags" : [
            {
                "name" : "hello world3",
                "id" : "hello world3"
            },
            {
                "name" : "hello world3",
                "id" : "hello world3"
            }
        ],
        "author" : {
            "email" : "g10guang@foxmail.com",
            "id" : "g10guang",
            "username" : "g10guang"
        },
        "createdTime" : "2017-09-13 09:07",
        "intro" : "psot3",
        "content" : "`psot3`",
        "title" : "hello world3",
        "id" : "60e0b807b58a49dfb2d3ebd7b0204c8a",
        "markdown" : "# Hello world",
        "status" : "craft",
        "rate" : 4.0,
        "browseNumber" : 20.0,
        "commentNumber" : 30.0,
        "likeNumber" : 49.0,
        "likeIPs" : [
            "127.0.0.1",
            "127.0.0.2",
            "10.139.31.161",
            "10.139.47.164"
        ],
        "comments" : []
    }
    :return: 0 -- 数据格式正确  -1 -- 缺少关键字  -2 -- 字段类型不对  -3 -- 附带了某些未定义的字段
    """
    try:
        assert '_id' not in article
        assert isinstance(article['tags'], list)
        for tag in article['tags']:
            assert isinstance(tag['name'], str)
            assert isinstance(tag['id'], str)
            assert len(tag) == 2
        assert isinstance(article['intro'], str)
        assert isinstance(article['content'], str)
        assert isinstance(article['title'], str)
        assert isinstance(article['id'], str)
        assert isinstance(article['markdown'], str)
        assert isinstance(article['status'], str)
        assert verify_article_status(article['status'])
    except KeyError:
        return -1
    except AssertionError:
        return -2
    else:
        if len(article) == 15:
            return 0
        return -3


def verify_project_format(project):
    """
    检查格式是否符合 project 数据格式
    {
    "_id" : ObjectId("59bc8b4d46172547b9691268"),
    "name" : "hello world",
    "intro" : "I want to say hello to the World.",
    "author" : [
        {
            "name" : "g10guang",
            "id" : "g10guang"
        }
    ],
    "tags" : [
        {
            "name" : "hello",
            "id" : "hello"
        },
        {
            "name" : "world",
            "id" : "world"
        }
    ],
    "isDel" : false,
    "createdTime" : "2017-09-16 10:24",
    "id" : "285919087c6346d2822a97d90eed494c",
    "projectURL" : "https://github.com/g10guang/whoyoungblog",
    "browseNumber" : 3
}
    :param project:
    :return: 0 -- 数据格式正确  -1 -- 缺少关键字  -2 -- 字段类型不对  -3 -- 附带了某些未定义的字段
    """
    try:
        assert '_id' not in project
        assert isinstance(project['name'], str)
        assert isinstance(project['author'], list)
        for author in project['author']:
            assert isinstance(author['name'], str)
            assert isinstance(author['id'], str)
            assert len(author) == 2
        assert isinstance(project['tags'], list)
        for tag in project['tags']:
            assert isinstance(tag['name'], str)
            assert isinstance(tag['id'], str)
            assert len(tag) == 2
        assert isinstance(project['isDel'], bool)
        assert isinstance(project['projectURL'], str)
    except KeyError:
        return -1
    except AssertionError:
        return -2
    else:
        if len(project) == 9:
            return 0


def verify_user_format(user):
    """
    检查格式是否符合 user 数据格式
    {
        "email" : "g10guang@foxmail.com",
        "intro" : "hello world",
        "oneText" : "hello world again",
        "introImgURL" : "https://avatars2.githubusercontent.com/u/18458140?v=4&u=32cc79ee4b8e2ba0992edb0c4976188a72de7d15&s=400",
        "socialAccount" : {
            "juejin" : "",
            "jianshu" : "",
            "github" : "https://github.com/g10guang"
        },
        "id" : "g10guang",
        "cryptPassword" : "80a4e02139201db1485380037adf8662",
        "username" : "g10guang",
        "type" : "admin",
        "signUpTime" : "2017-09-30 00:44",
        "status" : "normal",
        "articleNumber" : 10.0,
        "browseNumber" : 20.0,
        "commentNumber" : 30.0,
        "likeNumber" : 40.0,
    }
    :param user:
    :return: 0 -- 数据格式正确  -1 -- 缺少关键字  -2 -- 字段类型不对  -3 -- 附带了某些未定义的字段
    """
    try:
        assert '_id' not in user  # _id 应该由数据库生成
        assert isinstance(user['email'], str)
        assert re.match(EMAIL_REGEX, user['email'])
        assert isinstance(user['intro'], str)
        assert isinstance(user['introImgURL'], str)
        assert isinstance(user['socialAccount'], dict)
        assert isinstance(user['socialAccount']['juejin'], str)
        assert isinstance(user['socialAccount']['jianshu'], str)
        assert isinstance(user['socialAccount']['github'], str)
        assert len(user['socialAccount']) == 3
        assert isinstance(user['id'], str)
        assert isinstance(user['cryptPassword'], str)
        assert isinstance(user['username'], str)
        assert isinstance(user['type'], str)
        assert isinstance(user['signUpTime'], str)
        assert isinstance(user['status'], str)
        assert verify_user_status(user['status'])
        # mongodb 查询出来 float 即使是 int 类型
        assert isinstance(user['articleNumber'], float)
        assert isinstance(user['browseNumber'], float)
        assert isinstance(user['commentNumber'], float)
        assert isinstance(user['likeNumber'], float)
    except KeyError:
        # 缺少关键字
        return -1
    except AssertionError:
        # 字段类型不对
        return -2
    else:
        if len(user) == 15:
            return 0
        # 附带了某些未定义的字段
        return -3


def verify_edit_article_format(article):
    """
    检查更改文章字段的信息
    :return:
    """
    try:
        assert isinstance(article['intro'], str)
        assert verify_article_status(article['status'])
        assert isinstance(article['title'], str)
        assert isinstance(article['tags'], list)
        for t in article['tags']:
            assert isinstance(t, str)
        assert isinstance(article.get('markdown', ''), str)
        assert isinstance(article.get('content', ''), str)
    except KeyError:
        # 缺少关键字
        return -1
    except AssertionError:
        # 字段类型不对
        return -2
    else:
        # if len(article) == 4:
        #     return 0
        # 附带了某些没有定义的字段
        # return -3
        return 0


def check_str_contain_chinese(words):
    """
    检测字符串是否包含中文
    :param string:
    :return:
    """
    for ch in words:
        if 0x4e00 <= ord(ch) <= 0x9fff:
            return True
    return False


if __name__ == '__main__':
    from bson.objectid import ObjectId

    user = {
        "email": "g10guang@foxmail.com",
        "intro": "hello world",
        "oneText": "hello world again",
        "introImgURL": "https://avatars2.githubusercontent.com/u/18458140?v=4&u=32cc79ee4b8e2ba0992edb0c4976188a72de7d15&s=400",
        "socialAccount": {
            "juejin": "",
            "jianshu": "",
            "github": "https://github.com/g10guang"
        },
        "id": "g10guang",
        "cryptPassword": "80a4e02139201db1485380037adf8662",
        "username": "g10guang",
        "type": "admin",
        "signUpTime": "2017-09-30 00:44",
        "status": "normal",
        "articleNumber": 10.0,
        "browseNumber": 20.0,
        "commentNumber": 30.0,
        "likeNumber": 40.0,
    }

    # print(verify_user_format(user))

    article = {
        "tags": [
            {
                "name": "hello world3",
                "id": "hello world3"
            },
            {
                "name": "hello world3",
                "id": "hello world3"
            }
        ],
        "author": {
            "email": "g10guang@foxmail.com",
            "id": "g10guang",
            "username": "g10guang"
        },
        "createdTime": "2017-09-13 09:07",
        "intro": "psot3",
        "content": "`psot3`",
        "title": "hello world3",
        "id": "60e0b807b58a49dfb2d3ebd7b0204c8a",
        "markdown": "# Hello world",
        "status": "craft",
        "rate": 4.0,
        "browseNumber": 20.0,
        "commentNumber": 30.0,
        "likeNumber": 49.0,
        "likeIPs": [
            "127.0.0.1",
            "127.0.0.2",
            "10.139.31.161",
            "10.139.47.164"
        ],
        "comments": []
    }

    # print(verify_article_format(article))

    project = {
        "name": "hello world",
        "intro": "I want to say hello to the World.",
        "author": [
            {
                "name": "g10guang",
                "id": "g10guang"
            }
        ],
        "tags": [
            {
                "name": "hello",
                "id": "hello"
            },
            {
                "name": "world",
                "id": "world"
            }
        ],
        "isDel": False,
        "createdTime": "2017-09-16 10:24",
        "id": "285919087c6346d2822a97d90eed494c",
        "projectURL": "https://github.com/g10guang/whoyoungblog",
        "browseNumber": 3
    }

    # print(verify_project_format(project))
