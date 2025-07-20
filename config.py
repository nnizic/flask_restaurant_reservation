# config.py

import os


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost/restaurant"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "123tajni456kljuc789"
