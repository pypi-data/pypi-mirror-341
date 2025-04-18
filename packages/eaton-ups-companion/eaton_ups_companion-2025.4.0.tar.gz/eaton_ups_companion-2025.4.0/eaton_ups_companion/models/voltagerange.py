from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class VoltageRange:
    low: int
    high: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VoltageRange":
        return cls(
            low=data["low"],
            high=data["high"]
        )