from enum import Enum


class ExamType(Enum):
    MIDTERM = "Midterm"
    FINAL = "Final"
    QUIZ = "Quiz"


class HomeworkType(Enum):
    THEORY = "Theory"
    PRACTICAL = "Practical"


class homework_status(Enum):
    PENDING = "Pending"
    LATENCY = "Latency"
    ENDED = "Ended"


class hw_submission_status(Enum):
    SUBMITTED = "Submitted"
    NOT_SUBMITTED = "Not Submitted"


class exam_status(Enum):
    NOT_STARTED = "Not Started"
    ENDED = "Ended"
