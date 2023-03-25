import os

PROJECT_NAME:str = "Stack Experts Microservice"
PROJECT_VERSION: str = "1.0.0"

SEARCH_ENDPOINT_URL = os.getenv("ENDPOINT_URL", "https://ut6q88dndi.execute-api.eu-west-3.amazonaws.com/beta/")
USERS_ENDPOINT  = os.getenv("USERS_ENDPOINT", "None")