from fastapi import Path, APIRouter
from typing import List, Dict

from src.pydentic_models import ScheduledMessageBodyModel, ScheduledMessagesToDelete
from src.app_entities import AppScheduledMessage
from src.storage_acsses import storage_controller
from src.validations import validations


scheduled_messages_router = APIRouter(prefix="/scheduled_messages", tags=["Scheduled Messages"])


def send_multiple_scheduled_messages(scheduled_message: ScheduledMessageBodyModel) -> Dict:
    message_to_client = "The message wes sent to all recipients as requested"
    status_code = 200
    recipients_ids_that_received_message: List[str] = []
    recipients_ids_that_did_not_received_message: List[str] = []
    recipients_that_received_message_count = 0
    recipients_that_did_not_received_message_count = 0

    for recipient in scheduled_message.receivers_user_ids:
        if storage_controller.does_user_exist(recipient):
            new_scheduled_message = AppScheduledMessage(scheduled_message.sender_user_id, recipient,
                                                        scheduled_message.content,
                                                        scheduled_message.future_sending_time)
            storage_controller.save_scheduled_message(new_scheduled_message)
            recipients_ids_that_received_message.append(recipient)
            recipients_that_received_message_count += 1
        else:
            recipients_ids_that_did_not_received_message.append(recipient)
            recipients_that_did_not_received_message_count += 1

    if recipients_that_did_not_received_message_count > 0:
        status_code = 206
        message_to_client = f"{len(scheduled_message.receivers_user_ids)}" \
                            f" recipients were requested to send the message to," \
                            f" {recipients_that_received_message_count} recipients received message," \
                            f" {recipients_that_did_not_received_message_count} recipients did not received message."

    return {"message": {
        "message_to_client": message_to_client,
        "status code": status_code,
        "recipients_that_received_message_count": recipients_that_received_message_count,
        "recipients_ids_that_received_message": recipients_ids_that_received_message,
        "recipients_that_did_not_received_message_count": recipients_that_did_not_received_message_count,
        "recipients_ids_that_did_not_received_message": recipients_ids_that_did_not_received_message,
    }}


def delete_schedule_messages(messages_id_to_delete: ScheduledMessagesToDelete) -> Dict:
    message_to_client = "all messages were deleted as requested"
    status_code = 200
    deleted_messages_ids: List[str] = []
    not_found_messages_ids: List[str] = []
    count_deleted_messages = 0
    count_not_found_messages = 0

    for message_id in messages_id_to_delete.messages_ids:
        if storage_controller.does_scheduled_message_exist(message_id):
            scheduled_message_to_delete = storage_controller.retrieve_scheduled_messages_by_id(message_id)
            storage_controller.delete_scheduled_message(scheduled_message_to_delete)
            deleted_messages_ids.append(message_id)
            count_deleted_messages += 1
        else:
            not_found_messages_ids.append(message_id)
            count_not_found_messages += 1

    if count_not_found_messages > 0:
        status_code = 206
        message_to_client = f"{len(messages_id_to_delete.messages_ids)} messages sent for deletion," \
                            f" {count_deleted_messages} were found and deleted," \
                            f" {count_not_found_messages} were not found and therefore not deleted."

    return {"message": {
        "message_to_client": message_to_client,
        "status code": status_code,
        "count_deleted_messages": count_deleted_messages,
        "deleted_messages_ids": deleted_messages_ids,
        "count_not_found_messages_ids": count_not_found_messages,
        "not_found_messages_ids": not_found_messages_ids,
    }}


@scheduled_messages_router.post("/", status_code=202)
async def send_scheduled_message(scheduled_message: ScheduledMessageBodyModel):
    validations.raise_for_non_existing_message_sender(scheduled_message.sender_user_id)
    validations.raise_for_message_scheduled_to_past_time(scheduled_message.future_sending_time)
    return send_multiple_scheduled_messages(scheduled_message)


@scheduled_messages_router.delete("/", status_code=206)
def delete_scheduled_messages(messages_id_to_delete: ScheduledMessagesToDelete):
    return delete_schedule_messages(messages_id_to_delete)


@scheduled_messages_router.get("/{user_id}/{message_quantity}", status_code=200)
async def get_my_scheduled_messages(user_id: str, message_quantity: int = Path(default=1, gt=0)):
    validations.raise_for_non_existing_user(user_id)
    user_messages = storage_controller.retrieve_user_scheduled_messages(user_id, message_quantity)
    return {"message": user_messages}
