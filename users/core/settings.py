import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME:str = "Stack Experts - Users microservice"
PROJECT_VERSION: str = "1.0.0"

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./sql_app.db")

SECRET_KEY: str = os.getenv("SECRET_KEY", 'to_be_updated_soon')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES= 14 # in days

AMPQ_URL = os.getenv("AMPQ_URL")

############ POSTGRES config ##################
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

if POSTGRES_HOST:
    SQLALCHEMY_DATABASE_URL = DATABASE_URL