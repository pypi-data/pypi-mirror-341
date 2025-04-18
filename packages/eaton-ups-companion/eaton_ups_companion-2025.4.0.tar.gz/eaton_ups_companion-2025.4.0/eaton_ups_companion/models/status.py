from dataclasses import dataclass
from typing import Dict, Optional, Any

@dataclass
class Status:
    comLost: int
    product: str
    model: int
    serialNumber: Optional[Any]
    firmwareVersion: int
    nominalPower: int
    outputPower: int
    outputLoadLevel: int
    energy: int
    acPresent: int
    charging: int
    discharging: int
    batteryCapacity: int
    batteryRunTime: int
    remainingCapacityLimit: int
    runTimeToShutdown: int
    batteryTest: Optional[Any]
    overload: int
    outputStatus: int
    internalFailure: int
    batteryLow: int
    batteryFault: int
    shutdownImminent: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Status":
        return cls(
            comLost=data.get("comLost", 0),
            product=data.get("product", ""),
            model=data.get("model", 0),
            serialNumber=data.get("serialNumber"),
            firmwareVersion=data.get("firmwareVersion", 0),
            nominalPower=data.get("nominalPower", 0),
            outputPower=data.get("outputPower", 0),
            outputLoadLevel=data.get("outputLoadLevel", 0),
            energy=data.get("energy", 0),
            acPresent=data.get("acPresent", 0),
            charging=data.get("charging", 0),
            discharging=data.get("discharging", 0),
            batteryCapacity=data.get("batteryCapacity", 0),
            batteryRunTime=data.get("batteryRunTime", 0),
            remainingCapacityLimit=data.get("remainingCapacityLimit", 0),
            runTimeToShutdown=data.get("runTimeToShutdown", 0),
            batteryTest=data.get("batteryTest"),
            overload=data.get("overload", 0),
            outputStatus=data.get("outputStatus", 0),
            internalFailure=data.get("internalFailure", 0),
            batteryLow=data.get("batteryLow", 0),
            batteryFault=data.get("batteryFault", 0),
            shutdownImminent=data.get("shutdownImminent", 0)
        )