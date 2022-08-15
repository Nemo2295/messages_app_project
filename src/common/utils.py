from datetime import datetime
from uuid import uuid4


def generate_id() -> str:
    return str(uuid4())


def custom_format_of_current_datetime() -> str:
    return datetime.today().strftime("%d/%m/%Y %H:%M:%S")


def calculate_seconds_to_present_time(string_date: str) -> float:
    now = datetime.today()
    future_time = datetime.strptime(string_date, "%d/%m/%Y %H:%M:%S")
    differance = future_time - now
    return differance.total_seconds()
