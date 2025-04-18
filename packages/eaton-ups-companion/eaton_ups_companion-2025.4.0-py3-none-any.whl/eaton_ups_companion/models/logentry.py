from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class LogEntry:
    date: str
    level: int
    message: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEntry":
        return cls(
            date=data["date"],
            level=data["level"],
            message=data["message"]
        )