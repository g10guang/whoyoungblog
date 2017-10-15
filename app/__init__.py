import os

import gridfs
from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo

from app.config import load_config

# 配置日志
import logging

# 将日志输出到文件，方便服务器调试
log = logging.getLogger('debug')
fh = logging.FileHandler('debug.log', mode='w')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
log.setLevel(logging.DEBUG)
log.addHandler(fh)

SECRET_KEY_FILE = 'blog_secret_key'

app = Flask('whoyoungblog')

# gunicorn 同时启动多个 Flask 进程，只要 SECRET_KEY 保持一致，就可以共享 session
if not os.path.exists(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE, 'bw') as f:
        f.write(os.urandom(24))
with open(SECRET_KEY_FILE, 'br') as f:
    app.secret_key = f.read()  # session 用的 secret_key


app.config.from_object(load_config())

mongo = PyMongo(app, config_prefix='MONGODB')

with app.app_context():
    fs_grid = gridfs.GridFS(mongo.db, collection='fs')
    is_grid = gridfs.GridFS(mongo.db, collection='is')

login_manager = LoginManager(app)

from app.views import api, store

from app.views import apiview, objectstore
from app.admin import adminview
from app.search import searchapi

# Note: register blueprint should after import the views.
app.register_blueprint(store)
app.register_blueprint(api)

# 生产环境，设置 Sentry 错误报告
if os.environ.get('BLOG_MODE') == 'PRODUCT':
    from raven.contrib.flask import Sentry
    sentry = Sentry(app)

