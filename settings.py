'''
    配置类，会根据不同的场景配置不同的属性
'''

import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class DevelopConfig(object):
    SECRET_KEY = 'a random string'
    TOKEN_EXPIRATION = 600

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/api'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True