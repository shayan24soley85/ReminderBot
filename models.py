from dataclasses import dataclass
from typing import Optional

from Enums import ExamType


@dataclass
class Exam:
    course_name: str
    exam_type: str
    date_time: str
    location: Optional[str] = None


@dataclass
class Course:
    name: str
    professor: Optional[str] = None


@dataclass
class Reminder:
    user_id: int
    title: str
    date_time: str
    status: str = "Pending"


@dataclass
class ExamReminder(Reminder):
    course: Course
    exam_type: ExamType


@dataclass
class AssignmentReminder(Reminder):
    course: Course
    description: Optional[str] = None


@dataclass
class OtherUniReminder(Reminder):
    location: Optional[str] = None


@dataclass
class BirthdayReminder(Reminder):
    person_name: str
    relation: Optional[str] = None
