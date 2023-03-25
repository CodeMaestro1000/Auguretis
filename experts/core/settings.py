import os
from dotenv import load_dotenv

load_dotenv()

USERS_ENDPOINT = os.getenv("USERS_ENDPOINT", "None")
AMPQ_URL = os.getenv("AMPQ_URL")
REDIS_URL = os.getenv("REDIS_URL")
BIG_QUERY_CREDENTIALS_FILE = os.getenv("BIG_QUERY_CREDENTIALS_FILE")

PROJECT_NAME:str = "Stack Experts Microservice"
PROJECT_VERSION: str = "1.0.0"