import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or \
        "sqlite:///" + os.path.join(basedir, "instance", "app.db")

    SESSION_COOKIE_SECURE = False # Set to True in prod when using HTTPS
    SESSION_COOKIE_HTTPONLY = True #Prevent JS from accessing the cookie
    SESSION_COOKIE_SAMESITE = 'Lax'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    