from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SystemCfg:
    autoUpdateCheckInterval: int
    autoUpdateMode: str
    energyCost: int
    energyCurrency: str
    energyResetPeriod: str
    systemTray: int
    languageSelection: str
    languageList: Dict[str, str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SystemCfg":
        return cls(
            autoUpdateCheckInterval=data["autoUpdateCheckInterval"],
            autoUpdateMode=data["autoUpdateMode"],
            energyCost=data["energyCost"],
            energyCurrency=data["energyCurrency"],
            energyResetPeriod=data["energyResetPeriod"],
            systemTray=data["systemTray"],
            languageSelection=data["languageSelection"],
            languageList=data.get("languageList", {})
        )