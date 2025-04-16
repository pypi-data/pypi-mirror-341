"""
A2A SDK - Agent to Agent Protocol Python SDK
"""

__version__ = "0.1.0"

from a2a.types import (
    TaskState,
    TextPart,
    FilePart,
    DataPart,
    Message,
    TaskStatus,
    Artifact,
    Task,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
)

from a2a.client import A2AClient

__all__ = [
    "A2AClient",
    "TaskState",
    "TextPart",
    "FilePart",
    "DataPart",
    "Message",
    "TaskStatus",
    "Artifact",
    "Task",
    "TaskStatusUpdateEvent",
    "TaskArtifactUpdateEvent",
]
