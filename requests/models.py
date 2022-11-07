from enum import Enum
from typing import List

from pydantic import BaseModel, Field
from datetime import datetime, timezone


def generate_datetime_str() -> str:
    """
        (str): DateTime in ISO format.
    """
    return (datetime.utcnow()).replace(tzinfo=timezone.utc).isoformat()


class TestResult(Enum):
    UNKNOWN = "UNKNOWN"
    IN_PROGRESS = "IN_PROGRESS"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ABORTED = "ABORTED"
    QUEUED = "QUEUED"


class TestRunStartDTO(BaseModel):
    name: str
    started_at: str = Field(default_factory=generate_datetime_str())
    framework: str


class TestExecutionStartDTO(BaseModel):
    name: str
    class_name: str
    method_name: str
    started_at: str = Field(default_factory=generate_datetime_str())


class TestExecutionFinishDTO(BaseModel):
    result: str
    ended_at: str = Field(default_factory=generate_datetime_str())


class TestRunFinishDTO(BaseModel):
    ended_at: str = Field(default_factory=generate_datetime_str())


class LabelItemsDTO(BaseModel):
    key: str
    value: str


class TestRunLabelDTO(BaseModel):
    items: [List[str]]


class TestScreenshotsDTO(BaseModel):
    screenshot_array: bytearray


class LogDTO(BaseModel):
    test_id: str
    message: str
    level: str
    time_stamp: int


