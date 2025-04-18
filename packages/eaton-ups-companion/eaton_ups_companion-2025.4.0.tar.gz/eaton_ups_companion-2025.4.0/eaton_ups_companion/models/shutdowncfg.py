from dataclasses import dataclass
from typing import Dict, Optional, Any

@dataclass
class ShutdownCfg:
    powerSource: str
    shutdownEnabled: Optional[Any]
    loadSegment: int
    shutdownDuration: int
    shutdownTimer: int
    runTimeToEmptyLimit: int
    shutoffControl: int
    shutdownType: str
    shutdownScript: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ShutdownCfg":
        return cls(
            powerSource=data["powerSource"],
            shutdownEnabled=data.get("shutdownEnabled"),
            loadSegment=data["loadSegment"],
            shutdownDuration=data["shutdownDuration"],
            shutdownTimer=data["shutdownTimer"],
            runTimeToEmptyLimit=data["runTimeToEmptyLimit"],
            shutoffControl=data["shutoffControl"],
            shutdownType=data["shutdownType"],
            shutdownScript=data["shutdownScript"]
        )