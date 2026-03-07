import os 
from dotenv import load_dotenv

if os.getenv("TESTING"):
    load_dotenv(".env.test")
else:
    load_dotenv(".env")
class Config :
    SECRET_KEY  = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")