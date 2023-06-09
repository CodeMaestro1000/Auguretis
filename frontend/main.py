from fastapi import FastAPI
from config import settings
from fastapi.staticfiles import StaticFiles
from routes.main import frontend_router


def include_router(app):
	app.include_router(frontend_router)

def configure_static(app):  #new
    app.mount("/static", StaticFiles(directory="static"), name="static")

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    return app 


app = start_application()