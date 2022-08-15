from fastapi import Path, APIRouter

from src.pydentic_models import MessageBodyModel
from src.app_entities import AppRegularMessage
from src.storage_acsses import storage_controller
from src.validations import validations


regular_message_router = APIRouter(prefix="/regular_message", tags=["Regular Message"])


@regular_message_router.post("/", status_code=201)
async def send_message(message: MessageBodyModel):
    validations.raise_for_non_existing_message_sender(message.sender_user_id)
    validations.raise_for_non_existing_message_receiver(message.receiver_user_id)
    new_message = AppRegularMessage(message.sender_user_id, message.receiver_user_id, message.content)
    storage_controller.save_message(new_message)
    return {"message": new_message.message_id}


@regular_message_router.get("/{user_id}/{message_quantity}", status_code=200)
async def get_my_messages(user_id: str, message_quantity: int = Path(default=1, gt=0)):
    validations.raise_for_non_existing_user(user_id)
    user_messages = storage_controller.messages_by_user_id(user_id, message_quantity)
    return {"message": user_messages}
