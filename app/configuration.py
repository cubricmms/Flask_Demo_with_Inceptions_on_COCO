# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""


class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///flask'
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = "MINHACHAVESECRETA"
    CSRF_ENABLED = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Get your reCaptche key on: https://www.google.com/recaptcha/admin/create
# RECAPTCHA_PUBLIC_KEY = "6LffFNwSAAAAAFcWVy__EnOCsNZcG2fVHFjTBvRP"
# RECAPTCHA_PRIVATE_KEY = "6LffFNwSAAAAAO7UURCGI7qQ811SOSZlgU69rvv7"


class DevelopmentConfig(Config):
    DEBUG = True
