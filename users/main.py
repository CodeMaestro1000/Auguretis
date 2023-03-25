from fastapi import FastAPI
from core import settings
from db.session import engine
from db.database import Base 
from routes.users import user_router
from routes.login import login_router


def include_router(app):
    app.include_router(user_router, prefix="/users", tags=["users"])
    app.include_router(login_router, prefix="/login", tags=["login"])

def create_tables():
	Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    create_tables()
    return app

app = start_application()

