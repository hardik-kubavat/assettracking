import os

class Config(object):
    DEBUG = False
    #SQLALCHEMY_DATABASE_URI = "postgres:///testdb"
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY="admin"

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    
