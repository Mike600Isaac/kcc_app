class GeneralConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopmentConfig(GeneralConfig):
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@localhost/kcc_db"

class TestConfig(GeneralConfig):
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@localhost/kcc_db"