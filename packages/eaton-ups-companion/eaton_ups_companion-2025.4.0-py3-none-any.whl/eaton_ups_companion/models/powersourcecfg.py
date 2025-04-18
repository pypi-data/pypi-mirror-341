from dataclasses import dataclass
from typing import Dict, Optional, Any

@dataclass
class PowerSourceCfg:
    remainingCapacityLimitSetting: int
    outputVoltage: int
    outputSensitivityMode: Optional[Any]
    extendedVoltageMode: Optional[Any]
    inputVoltageRangeIndex: str
    ecoControlActivation: int
    ecoControlLevel: str
    audibleAlarm: int
    batteryTestSetting: Optional[Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PowerSourceCfg":
        return cls(
            remainingCapacityLimitSetting=data["remainingCapacityLimitSetting"],
            outputVoltage=data["outputVoltage"],
            outputSensitivityMode=data.get("outputSensitivityMode"),
            extendedVoltageMode=data.get("extendedVoltageMode"),
            inputVoltageRangeIndex=data["inputVoltageRangeIndex"],
            ecoControlActivation=data["ecoControlActivation"],
            ecoControlLevel=data["ecoControlLevel"],
            audibleAlarm=data["audibleAlarm"],
            batteryTestSetting=data.get("batteryTestSetting")
        )