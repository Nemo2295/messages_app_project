from pydantic import BaseModel, Field
from typing import Optional
from src.common import generate_id
from typing import List
from dynaconf import settings


MAX_MESSAGE_LENGTH = settings.get("REQUESTS_BODY_MODEL.max_message_length", 300)


class UserBodyModel(BaseModel):
    display_name: str = Field(example="Nemo1")
    first_name: str = Field(example="nimrod")
    last_name: str = Field(example="segev")
    middle_name: Optional[str] = Field(default=None, example="shlomo")


class MessageBodyModel(BaseModel):
    sender_user_id: str = Field(example=generate_id())
    receiver_user_id: str = Field(example=generate_id())
    content: str = Field(example="Hello", max_length=MAX_MESSAGE_LENGTH)


class ScheduledMessageBodyModel(BaseModel):
    sender_user_id: str = Field(example=generate_id())
    receivers_user_ids: List[str] = Field(example=[generate_id() for i in range(2)])
    content: str = Field(example="Future Hello", max_length=MAX_MESSAGE_LENGTH)
    future_sending_time: str = Field(example="04/07/2022 12:00:00", description="the format is %d/%m/%Y %H:%M:%S")


class ScheduledMessagesToDelete(BaseModel):
    messages_ids: List[str] = Field(example=[generate_id() for i in range(2)])


class UsersId(BaseModel):
    users_id: List[str] = Field(example=[generate_id() for i in range(2)])
