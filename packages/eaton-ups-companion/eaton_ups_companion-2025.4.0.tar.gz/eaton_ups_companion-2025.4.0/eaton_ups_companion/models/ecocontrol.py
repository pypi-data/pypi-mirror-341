from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EcoControl:
    low: int
    medium: int
    high: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EcoControl":
        return cls(
            low=data["low"],
            medium=data["medium"],
            high=data["high"]
        )