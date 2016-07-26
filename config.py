import os


class Config:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DELEGATED_ACCOUNT = os.environ['MR_DELEGATED_ACCOUNT']


class ProductionConfig(Config):
    DELEGATED_ACCOUNT = os.environ['MR_DELEGATED_ACCOUNT']

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
