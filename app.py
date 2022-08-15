from fastapi import responses, Request
from fastapi.responses import RedirectResponse
from dynaconf import settings
import asyncio

from factory import create_app
from src.common import RestableErrorBase
from src.storage_acsses import storage_controller


SCHEDULED_MESSAGE_WORKER_INTERVAL = settings.get("SENDING_SCHEDULED_MESSAGES.seconds", 7)


app = create_app()


async def send_scheduled_messages_in_time_intervals(seconds: int):
    while True:
        await storage_controller.send_scheduled_messages()
        await asyncio.sleep(seconds)


@app.on_event("startup")
def dispatch_background_tasks():
    asyncio.ensure_future(send_scheduled_messages_in_time_intervals(SCHEDULED_MESSAGE_WORKER_INTERVAL))


@app.exception_handler(RestableErrorBase)
async def handle_restable_error(_request: Request, error: RestableErrorBase) -> responses.JSONResponse:
    return responses.JSONResponse(error.to_json(), status_code=error.status_code)


@app.get("/", response_class=RedirectResponse, tags=["Home page"])
async def home_page():
    return "/docs#"
