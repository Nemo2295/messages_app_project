from src.common import custom_format_of_current_datetime, generate_id
from dataclasses import dataclass, field


@dataclass
class AppUser:
    display_name: str
    first_name: str
    last_name: str
    middle_name: str
    registration_date: str = field(default_factory=custom_format_of_current_datetime)
    user_id: str = field(default_factory=generate_id)
