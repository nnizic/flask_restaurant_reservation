# config.py

import os


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://giz73:naN1ca@localhost/restaurant"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "123tajni456kljuc789"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "project.virtualis@gmail.com"
    MAIL_PASSWORD = "jgbi mxri ygpt pnaz"
    MAIL_DEFAULT_SENDER = "project.virtualis@gmail.com"
