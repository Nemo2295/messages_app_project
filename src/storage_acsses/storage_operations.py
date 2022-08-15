from src.app_entities import AppUser, AppMessageBase, AppRegularMessage, AppScheduledMessage
from src.common import calculate_seconds_to_present_time
from abc import ABC, abstractmethod
from typing import Dict, List
from copy import copy


class UserStorageBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def init_storage(self):
        pass

    @abstractmethod
    def save_user(self, new_user: AppUser):
        pass

    @abstractmethod
    def delete_user(self, user_id: str):
        pass

    @abstractmethod
    def retrieve_all_users(self) -> Dict[str, AppUser]:
        pass

    @abstractmethod
    def does_user_exist(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def retrieve_user(self, user_id: str) -> AppUser:
        pass

    @abstractmethod
    def save_message(self, new_message: AppRegularMessage):
        pass

    @abstractmethod
    def messages_by_user_id(self, user_id: str, message_quantity: int) -> List[AppRegularMessage]:
        pass

    @abstractmethod
    def save_scheduled_message(self, new_scheduled_message: AppScheduledMessage):
        pass

    @abstractmethod
    def delete_scheduled_message(self, scheduled_message: AppScheduledMessage):
        pass

    @abstractmethod
    def retrieve_scheduled_messages_by_id(self, scheduled_message_id: str) -> AppScheduledMessage:
        pass

    @abstractmethod
    def retrieve_user_scheduled_messages(self, user_id: str, message_quantity: int) -> List[AppScheduledMessage]:
        pass

    @abstractmethod
    def does_scheduled_message_exist(self, scheduled_message_id: str) -> bool:
        pass

    @abstractmethod
    async def send_scheduled_messages(self):
        pass


class InMemoryStorage(UserStorageBase):
    def __init__(self):
        super().__init__()

    def init_storage(self):
        self._users: Dict[str, AppUser] = {}
        self._messages: Dict[str, List[AppMessageBase]] = {}
        self._scheduled_messages: List[AppScheduledMessage] = []

    def save_user(self, new_user: AppUser):
        self._users[new_user.user_id] = new_user
        self._messages[new_user.user_id] = []

    def delete_user(self, user_id: str):
        self._users.pop(user_id)
        self._messages.pop(user_id)

    def retrieve_all_users(self) -> Dict[str, AppUser]:
        all_users = copy(self._users)
        return all_users

    def does_user_exist(self, user_id: str) -> bool:
        for key in self._users:
            if key == user_id:
                return True
        return False

    def retrieve_user(self, user_id: str) -> AppUser:
        user = copy(self._users[user_id])
        return user

    def save_message(self, new_message: AppRegularMessage):
        self._messages[new_message.receiver_user_id].append(new_message)

    def messages_by_user_id(self, user_id: str, message_quantity: int) -> List[AppMessageBase]:
        user_messages = self._messages[user_id][:message_quantity]
        return user_messages

    def save_scheduled_message(self, new_scheduled_message: AppScheduledMessage):
        self._scheduled_messages.append(new_scheduled_message)

    def delete_scheduled_message(self, scheduled_message: AppScheduledMessage):
        self._scheduled_messages.remove(scheduled_message)

    def retrieve_scheduled_messages_by_id(self, scheduled_message_id: str) -> AppScheduledMessage:
        for scheduled_message in self._scheduled_messages:
            if scheduled_message.message_id == scheduled_message_id:
                return scheduled_message

    def retrieve_user_scheduled_messages(self, user_id: str, message_quantity: int) -> List[AppScheduledMessage]:
        user_scheduled_messages: List[AppScheduledMessage] = []

        for scheduled_message in self._scheduled_messages:
            if scheduled_message.sender_user_id == user_id:
                user_scheduled_messages.append(scheduled_message)

        return user_scheduled_messages[:message_quantity]

    def does_scheduled_message_exist(self, scheduled_message_id: str) -> bool:
        for message in self._scheduled_messages:
            if message.message_id == scheduled_message_id:
                return True
        return False

    async def send_scheduled_messages(self):
        scheduled_messages_sent: List[AppScheduledMessage] = []

        for scheduled_message in self._scheduled_messages:
            if calculate_seconds_to_present_time(scheduled_message.future_sending_time) < 0:
                scheduled_messages_sent.append(scheduled_message)

        for scheduled_message in scheduled_messages_sent:
            self._scheduled_messages.remove(scheduled_message)
            self._messages[scheduled_message.receiver_user_id].append(scheduled_message)
