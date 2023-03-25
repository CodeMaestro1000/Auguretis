from fastapi import FastAPI
from core import settings
from routes import search_router

def include_router(app):
	app.include_router(search_router)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    return app

app = start_application()