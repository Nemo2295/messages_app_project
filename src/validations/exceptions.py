from src.common import RestableErrorBase
import datetime


class UserErrorBase(RestableErrorBase):
    def __init__(self, message: str, status_code: int, user_id: str):
        super().__init__(message, status_code)
        self.user_id = user_id


class NonExistingUserError(UserErrorBase):
    MESSAGE = 'User does not exist'

    def __init__(self, status_code: int, user_id: str):
        super().__init__(self.MESSAGE, status_code, user_id)

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "user_id": str(self.user_id)
        }

    def __str__(self):
        return f'User with id {self.user_id} does not exists'


class ExistingUserError(UserErrorBase):
    MESSAGE = "Tried creating an already existing user"

    def __init__(self, status_code: int, user_id: str):
        super().__init__(self.MESSAGE, status_code, user_id)

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "user_id": str(self.user_id)
        }

    def __str__(self):
        return f"user with ID {self.user_id} already exist"


class MessageErrorBase(RestableErrorBase):
    pass


class NonExistingMessageReceiverError(MessageErrorBase):
    MESSAGE = "Message receiver is non existing user"

    def __init__(self, status_code: int, message_receiver_user_id: str):
        super().__init__(self.MESSAGE, status_code)
        self.message_receiver_user_id = message_receiver_user_id

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "message_receiver_user_id": self.message_receiver_user_id
        }

    def __str__(self):
        return f"trying to send a message to non existing user with ID {self.message_receiver_user_id}"


class NonExistingMessageSenderError(MessageErrorBase):
    MESSAGE = "Message sender is not an existing user"

    def __init__(self, status_code: int, message_sender_user_id: str):
        super().__init__(self.MESSAGE, status_code)
        self.message_sender_user_id = message_sender_user_id

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "message_sender_user_id": self.message_sender_user_id
        }

    def __str__(self):
        return f"trying to send a message to non existing user with ID {self.message_sender_user_id}"


class NonExistingScheduledMessageError(MessageErrorBase):
    MESSAGE = "Scheduled message id does not exist."

    def __init__(self, status_code: int, scheduled_message_id: str):
        super().__init__(self.MESSAGE, status_code)
        self.scheduled_message_id = scheduled_message_id

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "scheduled_message_id": str(self.scheduled_message_id)
        }

    def __str__(self):
        return f"trying to delete non existing message {self.scheduled_message_id}."


class SendingScheduledMessageToPastTimeError(MessageErrorBase):
    MESSAGE = f"trying to schedule a message to be sent before present time."

    def __init__(self, status_code: int, future_sending_time: str):
        super().__init__(self.MESSAGE, status_code)
        self.future_sending_time = future_sending_time

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "future_sending_time": self.future_sending_time,
        }

    def __str__(self):
        return f"trying to schedule a message to be sent before present time which is" \
               f" {datetime.datetime.today().strftime('%d/%m/%Y %H:%M:%S')}."
