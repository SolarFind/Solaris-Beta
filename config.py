class Configuration(object):
    SECRET_KEY = 'so_secret!'
    DEBUG = True
    SESSION_COOKIE_HTTPONLY = False
    TEMPLATES_AUTO_RELOAD = True
    #SQLALCHEMY_DATABASE_URI =
    SQLALCHEMY_DATABASE_URI = "sqlite:///FrontDB.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #SQLALCHEMY_POOL_SIZE = 100
    #SQLALCHEMY_POOL_RECYCLE = 280

BACK_URL = 'http://solarfind.net:8121'
#AUP Test