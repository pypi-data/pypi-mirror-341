from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SysInfo:
    code: str
    name: str
    manufacturer: str
    downloadLink: str
    vMajor: str
    vMinor: str
    vBuild: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SysInfo":
        return cls(
            code=data["code"],
            name=data["name"],
            manufacturer=data["manufacturer"],
            downloadLink=data["downloadLink"],
            vMajor=data["vMajor"],
            vMinor=data["vMinor"],
            vBuild=data["vBuild"]
        )