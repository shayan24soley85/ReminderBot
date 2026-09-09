from dataclasses import dataclass
from typing import Optional


@dataclass
class Reminder:
    user_id: int
    title: str
    date_time: str
    category: str
    status: str = "Pending"


@dataclass
class UniversityReminder(Reminder):
    event_type: str
    term: Optional[str] = None


@dataclass
class BirthdayReminder(Reminder):
    person_name: str
    relation: Optional[str] = None
