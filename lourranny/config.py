class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class Config:
    SECRET_KEY = 'uma-chave-secreta-e-unica'
