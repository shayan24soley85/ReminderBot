from dataclasses import dataclass
from typing import Optional

from Enums import (
    ExamType,
    HomeworkType,
    homework_status,
    hw_submission_status,
    exam_status,
)


@dataclass
class Exam:
    course: Course
    exam_type: ExamType
    date_time: str
    exam_status: exam_status
    location: Optional[str] = None


@dataclass
class Homework:
    course: Course
    homework_type: HomeworkType
    due_date: str
    status: homework_status
    submission_status: hw_submission_status
    description: Optional[str] = None


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
