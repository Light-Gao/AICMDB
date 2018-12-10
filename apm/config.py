#Some configurations must exist when application is running
#Different from enums/*.py.
class Config(object):
    """Base config class."""
    SECRET_KEY = '04204d5e2dfc22dd86090e0a8e964129'
    LOGGER_NAME = 'MiniCMDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    """Production config class."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://apm:abc123@10.10.100.98:3306/apm'


class DevConfig(Config):
    """Development config class."""
    # Open DEBUG mode
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://apm:abc123@10.10.100.98:3306/apm'
    CELERY_BROKER_URL = 'redis://127.0.0.1:8378/1'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:8378/2'
