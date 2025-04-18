from dataclasses import dataclass
from typing import Dict, Any, List
from . import EcoControl, VoltageRange

@dataclass
class DeviceInfo:
    product: str
    model: str
    country: str
    referenceNumber: str
    models: str
    name: str
    image: str
    ecoControlOutlet: int
    ecoControl: EcoControl
    inputVoltageRange: Dict[str, VoltageRange]
    outputVoltage: List[int]
    ecoControlOutletList: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeviceInfo":
        input_voltage_range = {
            key: VoltageRange.from_dict(value)
            for key, value in data.get("inputVoltageRange", {}).items()
        }
        return cls(
            product=data["product"],
            model=str(data["model"]),
            country=data["country"],
            referenceNumber=data["referenceNumber"],
            models=data["models"],
            name=data["name"],
            image=data["image"],
            ecoControlOutlet=data["ecoControlOutlet"],
            ecoControl=EcoControl.from_dict(data["ecoControl"]),
            inputVoltageRange=input_voltage_range,
            outputVoltage=data["outputVoltage"],
            ecoControlOutletList=data["ecoControlOutletList"]
        )