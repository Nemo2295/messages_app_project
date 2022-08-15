from src.common import custom_format_of_current_datetime, generate_id


class AppMessageBase:
    def __init__(self, sender_user_id: str, receiver_user_id: str, content: str):
        self.message_id: str = generate_id()
        self.request_time: str = custom_format_of_current_datetime()
        self.sender_user_id: str = sender_user_id
        self.receiver_user_id: str = receiver_user_id
        self.content: str = content


class AppRegularMessage(AppMessageBase):
    def __init__(self, sender_user_id: str, receiver_user_id: str, content: str):
        super().__init__(sender_user_id, receiver_user_id, content)
        self.sending_time: str = self.request_time


class AppScheduledMessage(AppMessageBase):
    def __init__(self, sender_user_id: str, receiver_user_id: str, content: str, future_sending_time: str):
        super().__init__(sender_user_id, receiver_user_id, content)
        self.future_sending_time: str = future_sending_time
