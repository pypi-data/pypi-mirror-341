from dataclasses import dataclass
from typing import Dict, Any, List
from . import LogEntry

@dataclass
class Logs:
    alarmCount: int
    logFile: str
    logList: List[LogEntry]
    max: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Logs":
        return cls(
            alarmCount=data["alarmCount"],
            logFile=data["logFile"],
            logList=[LogEntry.from_dict(item) for item in data.get("logList", [])],
            max=data["max"]
        )