from src.storage_acsses import storage_controller
from .exceptions import NonExistingUserError, NonExistingMessageReceiverError, \
    ExistingUserError, NonExistingMessageSenderError, \
    SendingScheduledMessageToPastTimeError, NonExistingScheduledMessageError
from src.common import calculate_seconds_to_present_time


def raise_for_non_existing_user(user_id: str):
    if not storage_controller.does_user_exist(user_id):
        raise NonExistingUserError(404, user_id)


def raise_for_existing_user(user_id: str):
    if storage_controller.does_user_exist(user_id):
        raise ExistingUserError(404, user_id)


def raise_for_non_existing_message_receiver(user_id: str):
    if not storage_controller.does_user_exist(user_id):
        raise NonExistingMessageReceiverError(404, user_id)


def raise_for_non_existing_message_sender(user_id: str):
    if not storage_controller.does_user_exist(user_id):
        raise NonExistingMessageSenderError(404, user_id)


def raise_for_message_scheduled_to_past_time(future_sending_time: str):
    if calculate_seconds_to_present_time(future_sending_time) < 0:
        raise SendingScheduledMessageToPastTimeError(403, future_sending_time)


def raise_for_non_existing_scheduled_message(message_id: str):
    if not storage_controller.does_scheduled_message_exist(message_id):
        raise NonExistingScheduledMessageError(404, message_id)
