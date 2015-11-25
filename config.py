__author__ = 'Kumar_Garg'

class Config(object):
    SECRET_KEY = '1qlUcb4T7DFDpp5vv3_'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///catalog'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


