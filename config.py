import os


class Config:
    @staticmethod
    def init_app(app):
        pass

    DELEGATED_ACCOUNT = os.environ['MR_DELEGATED_ACCOUNT']


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
