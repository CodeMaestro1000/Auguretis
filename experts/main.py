from fastapi import FastAPI
from core import settings
from google.cloud import bigquery
from google.oauth2 import service_account
from core.settings import BIG_QUERY_CREDENTIALS_FILE

credentials = service_account.Credentials.from_service_account_file(BIG_QUERY_CREDENTIALS_FILE)
# Not used in k8s deployment

client = bigquery.Client(credentials=credentials)

from routes import expert_router # to prevent circular import

def include_router(app):
	app.include_router(expert_router)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    return app

app = start_application()
