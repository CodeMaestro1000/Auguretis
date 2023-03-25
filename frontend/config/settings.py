import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_NAME: str = "Stack Experts - Frontend microservice"
PROJECT_VERSION: str = "1.0.0"

USERS_ENDPOINT = os.getenv("USERS_ENDPOINT", "http://127.0.0.1:8000") # remove default!!!
AMPQ_URL = os.getenv("AMPQ_URL")