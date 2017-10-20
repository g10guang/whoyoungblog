#!/usr/bin/env python3
# coding=utf-8
# author: Xiguang Liu<g10guang@foxmail.com>
# 2017-09-11 11:08

from flask import Blueprint

api = Blueprint('api', 'api', subdomain='api')

RANDOM_IMG_DEFAULT_URL = 'http://uk.france.fr/sites/default/files/imagecache/ATF_Image_bandeau_v2/la_france_cote_nature_1.jpg'