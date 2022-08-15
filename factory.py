from fastapi import FastAPI
from src.storage_acsses import storage_controller
from dynaconf import settings
from src.endpoints import users_router, regular_message_router, scheduled_messages_router, db_users_router


APP_TITLE = settings.get("FASTAPI.title", "message app")
APP_DESCRIPTION = settings.get("FASTAPI.description", "message app using fastapi")
APP_VERSION = settings.get("FASTAPI.version", "0.0.1")
APP_CONTACT_NAME = settings.get("FASTAPI.CONTACT.name", "jane doe")
APP_CONTACT_EMAIL = settings.get("FASTAPI.CONTACT.email", "janedoe@gmail.com")

APP_SUB_ROUTES = [users_router, regular_message_router, scheduled_messages_router, db_users_router]


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION, version=APP_VERSION,
                           contact={"name": APP_CONTACT_NAME, "email": APP_CONTACT_EMAIL})
    storage_controller.init_storage()

    for route in APP_SUB_ROUTES:
        app.include_router(route)

    return app
