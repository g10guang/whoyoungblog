#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-13 10:47

from bson.objectid import ObjectId

from app import mongo


class Admin:
    def __init__(self, active=True, authenticated=True, **kwargs) -> None:
        super().__init__()
        self.active = active
        self.authenticated = authenticated
        if '_id' in kwargs and isinstance(kwargs['_id'], ObjectId):
            kwargs['_id'] = str(kwargs['_id'])
        for k, v in kwargs.items():
            setattr(self, k, v)

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return self._id

    @staticmethod
    def find_by_username(username):
        admin_dict = mongo.db.admins.find_one({'username': username})
        return Admin(**admin_dict)

    @staticmethod
    def find_by_email(email):
        admin_dict = mongo.db.admins.find_one({'email': email})
        return Admin(**admin_dict)

    @staticmethod
    def find_by_oid(oid):
        if isinstance(oid, str):
            oid = ObjectId(oid)
        admin_dict = mongo.db.admins.find_one({'_id': oid})
        return Admin(**admin_dict)