import os

class Config:
    SECRET_KEY = "change-this-secret-should-be-32-bytes-min-1234"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.dirname(__file__), 'instance', 'placement.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "your-secret-key-should-be-at-least-32-bytes-long-for-sha256-1234567890"
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = "redis://localhost:6379/1"
    CACHE_DEFAULT_TIMEOUT = 300
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_DEFAULT_SENDER = "noreply@placementportal.com"
